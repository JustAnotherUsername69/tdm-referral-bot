from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def join_keyboard(link):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Join Channel", url=link)],
        [InlineKeyboardButton("✅ I’ve Joined / Refresh", callback_data="refresh")]
    ])

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 My Stats", callback_data="stats")],
        [InlineKeyboardButton("🔗 Refer & Earn", callback_data="refer")],
        [InlineKeyboardButton("💰 Redeem Points", callback_data="redeem")],
        [InlineKeyboardButton("🎁 My Coupons", callback_data="coupons")]
    ])
