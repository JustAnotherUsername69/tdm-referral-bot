from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)

from bot.config import BOT_TOKEN
from bot.handlers.start import start
from bot.handlers.admin import admin_stats, broadcast, add_coupons
from bot.handlers.callbacks import callbacks
from bot.handlers.redeem import redeem_text
from bot.handlers.admin_input import admin_input

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", admin_stats))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("addcoupons", add_coupons))

# Buttons
app.add_handler(CallbackQueryHandler(callbacks))

# Admin input (broadcast / addcoupons)
app.add_handler(
    MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL,
        admin_input
    )
)

# User redeem input
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, redeem_text)
)

app.run_polling()
