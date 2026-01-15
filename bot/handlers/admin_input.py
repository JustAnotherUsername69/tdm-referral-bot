from bot.db import get_conn
from bot.config import ADMIN_ID
from datetime import datetime

async def admin_input(update, context):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.user_data:
        return

    mode = context.user_data.get("mode")

    conn = get_conn()
    cur = conn.cursor()

    # ---------------- BROADCAST ----------------
    if mode == "broadcast":
        msg = update.message

        payload_type = "text"
        payload_text = msg.text
        payload_file_id = None

        if msg.photo:
            payload_type = "photo"
            payload_file_id = msg.photo[-1].file_id
            payload_text = msg.caption
        elif msg.video:
            payload_type = "video"
            payload_file_id = msg.video.file_id
            payload_text = msg.caption
        elif msg.document:
            payload_type = "document"
            payload_file_id = msg.document.file_id
            payload_text = msg.caption

        cur.execute("""
            INSERT INTO broadcasts
            (admin_id, payload_type, payload_text, payload_file_id)
            VALUES (%s,%s,%s,%s)
        """, (
            update.effective_user.id,
            payload_type,
            payload_text,
            payload_file_id
        ))
        conn.commit()
        conn.close()

        context.user_data.clear()
        await update.message.reply_text("✅ Broadcast queued successfully.")
        return

    # ---------------- ADD COUPONS ----------------
    if mode == "addcoupons":
        lines = [l.strip() for l in update.message.text.splitlines() if l.strip()]
        added = 0

        for code in lines:
            try:
                cur.execute(
                    "INSERT INTO coupons (code) VALUES (%s)",
                    (code,)
                )
                added += 1
            except:
                pass  # duplicate ignored

        conn.commit()
        conn.close()

        context.user_data.clear()
        await update.message.reply_text(
            f"✅ Added {added} new coupons.\n"
            f"❌ Duplicates ignored."
        )
