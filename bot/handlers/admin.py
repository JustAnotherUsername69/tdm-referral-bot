from bot.db import get_conn
from bot.config import ADMIN_ID, BROADCAST_LOG_CHANNEL
from datetime import datetime

async def admin_stats(update, context):
    if update.effective_user.id != ADMIN_ID:
        return

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM coupons WHERE used=false")
    available = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM coupons WHERE used=true")
    used = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM broadcasts WHERE status='running'")
    running = cur.fetchone()[0]

    conn.close()

    await update.message.reply_text(
        f"📊 Admin Stats\n\n"
        f"👥 Users: {users}\n"
        f"🎟 Available Coupons: {available}\n"
        f"✅ Used Coupons: {used}\n"
        f"📣 Broadcasts running: {running}"
    )

async def broadcast(update, context):
    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data.clear()
    context.user_data["mode"] = "broadcast"
    await update.message.reply_text("📣 Send the message or media to broadcast.")

async def add_coupons(update, context):
    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data.clear()
    context.user_data["mode"] = "addcoupons"
    await update.message.reply_text(
        "🧾 Send coupon codes, one per line.\n"
        "Duplicates will be ignored."
    )
