from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from bot.config import BOT_TOKEN
from bot.handlers.start import start
from bot.handlers.admin import admin_stats, broadcast

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", admin_stats))
app.add_handler(CommandHandler("broadcast", broadcast))

app.run_polling()
