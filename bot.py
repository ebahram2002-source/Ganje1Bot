from database import add_movie, get_movie
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8931502232:AAG-BZy0HOWSEPKSW_JnPUJvosNYov7cgBw"

CHANNEL_USERNAME = "@blackempire_vip"
CHANNEL_ID = -100263904710

# ذخیره موقت فیلم‌ها (فعلاً ساده)
movies = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args:
        movie_id = args[0]
        context.user_data["movie_id"] = movie_id

        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("✅ بررسی عضویت", callback_data="check")]
        ]

        await update.message.reply_text(
            "برای دریافت فیلم باید عضو کانال شوید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("به ربات خوش آمدی 🎬")

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)

        if member.status in ["member", "creator", "administrator"]:
            movie_id = get_movie(movie_id)

            if movie_id:
               await context.bot.copy_message(
    chat_id=user_id,
   from_chat_id=CHANNEL_ID,
message_id=movie_id
)
            else:
                await query.message.reply_text("فیلمی انتخاب نشده است.")
        else:
            await query.message.reply_text("❌ هنوز عضو کانال نشده‌اید.")

    except:
        await query.message.reply_text("خطا در بررسی عضویت. دوباره تلاش کنید.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_membership))

    app.run_polling()

if __name__ == "__main__":
    main()
