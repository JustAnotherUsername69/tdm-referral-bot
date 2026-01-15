from datetime import datetime
from bot.db import get_conn
from bot.config import REDEEM_INSTRUCTIONS, COUPON_LOG_CHANNEL

async def redeem_text(update, context):
    if context.user_data.get("mode") != "redeem":
        return

    uid = update.effective_user.id
    text = update.message.text.strip()

    try:
        points = int(text)
        if points <= 0:
            raise ValueError
    except:
        await update.message.reply_text("❌ Enter a valid number.")
        return

    conn = get_conn()
    cur = conn.cursor()

    # Get balance
    cur.execute(
        "SELECT points FROM users WHERE user_id=%s",
        (uid,)
    )
    row = cur.fetchone()
    if not row or row[0] < points:
        conn.close()
        await update.message.reply_text("❌ Insufficient points.")
        return

    # Calculate coupon count
    coupons_needed = 12 if points == 10 else 6 if points == 5 else points

    try:
        # Atomic coupon selection
        cur.execute("""
            SELECT id, code FROM coupons
            WHERE used = false
            LIMIT %s
            FOR UPDATE SKIP LOCKED
        """, (coupons_needed,))
        coupons = cur.fetchall()

        if len(coupons) < coupons_needed:
            conn.rollback()
            await update.message.reply_text("❌ Coupons out of stock.")
            return

        for cid, code in coupons:
            cur.execute("""
                UPDATE coupons
                SET used=true, used_by=%s, used_at=%s
                WHERE id=%s
            """, (uid, datetime.utcnow(), cid))

            cur.execute("""
                INSERT INTO coupon_history (user_id, code, redeemed_at)
                VALUES (%s,%s,%s)
            """, (uid, code, datetime.utcnow()))

        cur.execute(
            "UPDATE users SET points = points - %s WHERE user_id=%s",
            (points, uid)
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    # Send coupons
    msg = "🎉 Your Coupons\n\n"
    for _, code in coupons:
        msg += f"{code}\n"

    msg += "\n" + REDEEM_INSTRUCTIONS
    await update.message.reply_text(msg)

    # Log
    await context.bot.send_message(
        COUPON_LOG_CHANNEL,
        f"User {uid} redeemed {points} points"
    )

    context.user_data.clear()
