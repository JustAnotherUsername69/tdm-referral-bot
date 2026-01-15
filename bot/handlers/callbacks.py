from bot.db import get_conn
from bot.keyboards import main_menu, join_keyboard
from bot.config import CHANNEL_ID

async def callbacks(update, context):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    # Subscription refresh
    if query.data == "refresh":
        try:
            member = await context.bot.get_chat_member(CHANNEL_ID, uid)
            if member.status in ("member", "administrator", "creator"):
                await query.message.reply_text(
                    "✅ Subscription verified!",
                    reply_markup=main_menu()
                )
            else:
                raise Exception
        except:
            await query.message.reply_text(
                "❌ Still not subscribed.",
                reply_markup=join_keyboard("https://t.me/+s3SQO0QOY_wwZDQ1")
            )
        return

    # Block features if not subscribed
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, uid)
        if member.status not in ("member", "administrator", "creator"):
            raise Exception
    except:
        await query.message.reply_text(
            "❌ Join channel to continue.",
            reply_markup=join_keyboard("https://t.me/+s3SQO0QOY_wwZDQ1")
        )
        return

    conn = get_conn()
    cur = conn.cursor()

    # User stats
    if query.data == "stats":
        cur.execute(
            "SELECT referrals, points FROM users WHERE user_id=%s",
            (uid,)
        )
        r, p = cur.fetchone()
        await query.message.reply_text(
            f"📊 Your Stats\n\nReferrals: {r}\nPoints: {p}"
        )

    # Referral link
    elif query.data == "refer":
        await query.message.reply_text(
            f"🔗 Your referral link:\n"
            f"https://t.me/TDMReferralRewardsBot?start={uid}"
        )

    # Redeem
    elif query.data == "redeem":
        context.user_data.clear()
        context.user_data["mode"] = "redeem"
        await query.message.reply_text(
            "💰 Enter number of points to redeem:"
        )

    # Coupon history
    elif query.data == "coupons":
        cur.execute(
            "SELECT code, redeemed_at FROM coupon_history WHERE user_id=%s",
            (uid,)
        )
        rows = cur.fetchall()
        if not rows:
            await query.message.reply_text("❌ No coupons redeemed yet.")
        else:
            msg = "🎁 Your Coupons\n\n"
            for c, d in rows:
                msg += f"{c} — {d}\n"
            await query.message.reply_text(msg)

    conn.close()
