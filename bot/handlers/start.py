from datetime import datetime
from bot.db import get_conn
from bot.keyboards import join_keyboard, main_menu
from bot.config import CHANNEL_ID

async def start(update, context):
    user = update.effective_user
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (user_id, username, first_seen) VALUES (%s,%s,%s) "
        "ON CONFLICT (user_id) DO NOTHING",
        (user.id, user.username, datetime.utcnow())
    )
    conn.commit()
    conn.close()

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user.id)
        if member.status not in ("member", "administrator", "creator"):
            raise Exception
    except:
        await update.message.reply_text(
            "❌ Join channel to continue.",
            reply_markup=join_keyboard("https://t.me/+s3SQO0QOY_wwZDQ1")
        )
        return

    await update.message.reply_text(
        "✅ Welcome to TDM Referral Rewards Bot",
        reply_markup=main_menu()
    )
