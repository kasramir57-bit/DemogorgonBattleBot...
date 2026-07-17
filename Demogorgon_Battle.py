import json
import os
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = "8664147203:AAE5h65NMoehj35LyLm71A4mEW2LEj-FvWw"

DATABASE = "database.json"


# ======================
# دیتابیس
# ======================

def load_players():
    if not os.path.exists(DATABASE):
        return {}

    with open(DATABASE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_players():
    with open(DATABASE, "w", encoding="utf-8") as file:
        json.dump(
            players,
            file,
            ensure_ascii=False,
            indent=4
        )


players = load_players()


# ======================
# دموگورگون
# ======================

demogorgon = {
    "hp": 5000,
    "alive": True
}


# ======================
# سلاح‌ها
# ======================

weapons = {
    "چاقوی ساده": 50,
    "شمشیر آهنی": 100,
    "تبر جنگی": 180,
    "شمشیر دموگورگون": 300
}


shop_weapons = {
    "شمشیر آهنی": 200,
    "تبر جنگی": 400,
    "شمشیر دموگورگون": 800
}


# ======================
# دستورات اصلی
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👹 به نبرد دموگورگون خوش آمدی!\n\n"
        "برای شروع بازی /join را بزن."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 راهنمای بازی:\n\n"
        "/join ورود به بازی\n"
        "/profile پروفایل\n"
        "/attack حمله به دموگورگون\n"
        "/weapon سلاح فعلی\n"
        "/inventory وسایل\n"
        "/shop فروشگاه\n"
        "/buy خرید سلاح\n"
        "/equip انتخاب سلاح"
    )


async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌌 داستان:\n\n"
        "دموگورگون از دنیای وارونه وارد شده است.\n"
        "بازیکنان باید با همکاری او را شکست دهند."
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏓 ربات فعال است."
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    if uid in players:
        await update.message.reply_text(
            "⚔️ تو قبلاً وارد بازی شدی!"
        )
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

    save_players()

    await update.message.reply_text(
        f"✅ {user.first_name} وارد نبرد شد!\n\n"
        "❤️ HP: 100\n"
        "⭐ Level: 1\n"
        "🪙 Coin: 100"
    )


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if uid not in players:
        await update.message.reply_text(
            "اول /join بزن"
        )
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


# ======================
# نبرد دموگورگون
# ======================

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if uid not in players:
        await update.message.reply_text(
            "اول /join بزن"
        )
        return

    if not demogorgon["alive"]:
        await update.message.reply_text(
            "👹 دموگورگون شکست خورده است!"
        )
        return

    current_weapon = players[uid]["weapon"]

    power = weapons.get(
        current_weapon,
        50
    )

    damage = random.randint(
        power,
        power + 50
    )

    demogorgon["hp"] -= damage

    players[uid]["xp"] += damage
    players[uid]["coin"] += 10

    save_players()

    if demogorgon["hp"] <= 0:
        demogorgon["hp"] = 0
        demogorgon["alive"] = False

        await update.message.reply_text(
            "🔥🔥 پیروزی بزرگ 🔥🔥\n\n"
            "👹 دموگورگون نابود شد!"
        )
        return

    await update.message.reply_text(
        f"⚔️ حمله با {current_weapon}\n\n"
        f"💥 آسیب: {damage}\n"
        f"👹 HP دموگورگون: {demogorgon['hp']}\n\n"
        f"⭐ XP +{damage}\n"
        f"🪙 Coin +10"
    )


# ======================
# سلاح و Inventory
# ======================

async def weapon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if uid not in players:
        await update.message.reply_text(
            "اول /join بزن"
        )
        return

    w = players[uid]["weapon"]

    await update.message.reply_text(
        f"🗡 سلاح فعلی:\n{w}\n"
        f"💥 قدرت: {weapons.get(w,50)}"
    )


async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if uid not in players:
        await update.message.reply_text(
            "اول /join بزن"
        )
        return

    text = "🎒 Inventory:\n\n"

    for item in players[uid]["inventory"]:
        text += f"🗡 {item}\n"

    await update.message.reply_text(text)


# ======================
# فروشگاه
# ======================

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🛒 فروشگاه:\n\n"

    for name, price in shop_weapons.items():
        text += f"🗡 {name} = 🪙 {price}\n"

    text += "\nخرید:\n/buy نام سلاح"

    await update.message.reply_text(text)


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if uid not in players:
        await update.message.reply_text(
            "اول /join بزن"
        )
        return

    if not context.args:
        await update.message.reply_text(
            "اسم سلاح را بعد از /buy بنویس"
        )
        return

    name = " ".join(context.args)

    if name not in shop_weapons:
        await update.message.reply_text(
            "❌ این سلاح وجود ندارد"
        )
        return

    price = shop_weapons[name]

    if players[uid]["coin"] < price:
        await update.message.reply_text(
            "🪙 پول کافی نداری"
        )
        return

    players[uid]["coin"] -= price
    players[uid]["inventory"].append(name)

    save_players()

    await update.message.reply_text(
        f"✅ خرید شد:\n{name}"
        )

# ======================
# انتخاب سلاح
# ======================

async def equip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if uid not in players:
        await update.message.reply_text(
            "اول /join بزن"
        )
        return

    if not context.args:
        await update.message.reply_text(
            "مثال:\n/equip شمشیر آهنی"
        )
        return

    weapon_name = " ".join(context.args)

    if weapon_name not in players[uid]["inventory"]:
        await update.message.reply_text(
            "❌ این سلاح را نداری"
        )
        return

    players[uid]["weapon"] = weapon_name

    save_players()

    await update.message.reply_text(
        f"✅ سلاح انتخاب شد:\n🗡 {weapon_name}"
    )


# ======================
# اجرای ربات
# ======================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("story", story))
    app.add_handler(CommandHandler("ping", ping))

    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("profile", profile))

    app.add_handler(CommandHandler("attack", attack))

    app.add_handler(CommandHandler("weapon", weapon))
    app.add_handler(CommandHandler("inventory", inventory))

    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("buy", buy))

    app.add_handler(CommandHandler("equip", equip))


    app.run_polling()


if __name__ == "__main__":
    main()
