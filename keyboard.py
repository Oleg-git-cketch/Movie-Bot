from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎬 Фильмы"))
    return markup

def sponsors_keyboard(sponsors):
    markup = InlineKeyboardMarkup()
    for channel in sponsors:
        markup.add(InlineKeyboardButton(f"Подписаться на {channel}", url=f"https://t.me/{channel[1:]}"))
    markup.add(InlineKeyboardButton("✅ Проверить подписку", callback_data="check_subs"))
    return markup
