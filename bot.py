import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = "8926193650:AAEwLF6bGDnQFQnhcy4AoBcAigAB8RrTHJM"
OWNER_LINK = "https://t.me/ACIDITYYAK"

# 🔹 Instant /start Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_card = (
        "<b>🌹 Welcome Sir! Main Aapka Super-Fast Group Manager Bot Hoon.</b>\n\n"
        "⚡ <b>Engine Status:</b> Rocket Speed (0.1s)\n"
        "🛡️ <b>Security:</b> Auto Anti-Link Shield Active.\n\n"
        "<i>Niche diye gaye buttons se bot ko control karein:</i>"
    )
    keyboard = [
        [InlineKeyboardButton("📜 Help Manual", callback_data="help"), InlineKeyboardButton("ℹ️ About Bot", callback_data="about")],
        [InlineKeyboardButton("👑 Owner Profile", url=OWNER_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_card, parse_mode="HTML", reply_markup=reply_markup)

# 🔹 Instant /help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_card = (
        "<b>📖 Help Manual, Sir:</b>\n\n"
        "🔸 <code>/start</code> - Bot ka welcome message.\n"
        "🔸 <code>/help</code> - Commands guide.\n"
        "🔸 <code>/about</code> - Owner & Bot info.\n\n"
        "🛡️ <i>Group me links auto-delete karne ke liye bot ko Admin banayein.</i>"
    )
    await update.message.reply_text(help_card, parse_mode="HTML")

# 🔹 Instant /about Command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_card = (
        "<b>ℹ️ About Ebaadda Bot, Sir:</b>\n\n"
        "🤖 <b>Bot Name:</b> EBA ADDA Manager\n"
        "⚡ <b>Speed:</b> Instant High-Speed Engine\n"
        "🛡️ <b>Security:</b> Anti-Link & Moderation\n\n"
        "<i>Designed to keep your groups safe and active!</i>"
    )
    keyboard = [[InlineKeyboardButton("👑 Contact Owner", url=OWNER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(about_card, parse_mode="HTML", reply_markup=reply_markup)

# 🔹 Instant Anti-Link (Bina Kisi Delay Ke)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    chat_id = update.effective_chat.id
    user_id = user.id
    user_name = user.mention_html()
    user_text = update.message.text or ""
    chat_type = update.effective_chat.type

    if chat_type in ['group', 'supergroup']:
        has_link = any(link in user_text.lower() for link in ["http://", "https://", "t.me/", "telegram.me/", ".com", ".in"])
        if has_link:
            try:
                await update.message.delete()
                await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                await context.bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
                await context.bot.send_message(chat_id=chat_id, text=f"⚠️ {user_name} Sir ko remove kar diya gaya hai (Anti-Link)!", parse_mode="HTML")
                return
            except TelegramError:
                pass

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Maximum Speed Engine Active!")
    app.run_polling()
