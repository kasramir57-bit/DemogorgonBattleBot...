from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8664147203:AAE5h65NMoehj35LyLm71A4mEW2LEj-FvWw"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👹 به نبرد دموگورگون خوش آمدی!\n\n"
        "برای ورود به بازی دستور /join را بزن."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 دستورات بازی:\n\n"
        "/join - ورود به بازی\n"
        "/story - داستان بازی\n"
        "/ping - تست ربات"
    )


async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌌 دموگورگون از دنیای وارونه آمده است.\n"
        "بازیکنان باید با همکاری آن را شکست دهند."
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 ربات فعال است.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("story", story))
    app.add_handler(CommandHandler("ping", ping))

    app.run_polling()


if __name__ == "__main__":
    main()
