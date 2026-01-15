from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)

from bot.config import BOT_TOKEN
from bot.handlers.start import start
from bot.handlers.admin import admin_stats, broadcast
from bot.handlers.callbacks import callbacks
from bot.handlers.redeem import redeem_text

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", admin_stats))
app.add_handler(CommandHandler("broadcast", broadcast))

# Buttons
app.add_handler(CallbackQueryHandler(callbacks))

# Redeem input (text only, no commands)
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, redeem_text)
)

app.run_polling()
