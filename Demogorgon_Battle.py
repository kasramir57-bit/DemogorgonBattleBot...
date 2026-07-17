import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8664147203:AAE5h65NMoehj35LyLm71A4mEW2LEj-FvWw"

DATABASE = "database.json"


def load_players():
    if not os.path.exists(DATABASE):
        return {}

    with open(DATABASE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_players(players):
    with open(DATABASE, "w", encoding="utf-8") as file:
        json.dump(players, file, ensure_ascii=False, indent=4)


players = load_players()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👹 به نبرد دموگورگون خوش آمدی!\n\n"
        "برای ورود به بازی:\n"
        "/join"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 دستورات:\n\n"
        "/join ورود به بازی\n"
        "/story داستان\n"
        "/ping تست ربات\n"
        "/profile پروفایل"
    )


async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌌 دنیای وارونه باز شده است.\n"
        "دموگورگون آماده نبرد است..."
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 ربات روشن است")


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    if uid in players:
        await update.message.reply_text("⚔️ قبلاً وارد بازی شدی!")
        return

    players[uid] = {
        "name": user.first_name,
        "hp": 100,
        "level": 1,
        "xp": 0,
        "coin": 100,
        "weapon": "چاقوی ساده",
        "inventory": [
            "چاقوی ساده"
        ]
    }

    save_players(players)

    await update.message.reply_text(
        f"✅ {user.first_name} وارد نبرد شد!\n\n"
        "❤️ HP: 100\n"
        "⭐ Level: 1\n"
        "🪙 Coin: 100"
    )


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if uid not in players:
        await update.message.reply_text("اول /join بزن")
        return

    p = players[uid]

    await update.message.reply_text(
        f"👤 پروفایل\n\n"
        f"❤️ HP: {p['hp']}\n"
        f"⭐ Level: {p['level']}\n"
        f"✨ XP: {p['xp']}\n"
        f"🪙 Coin: {p['coin']}\n"
        f"🗡 سلاح: {p['weapon']}"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("story", story))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("profile", profile))

    app.run_polling()


if __name__ == "__main__":
    main()
