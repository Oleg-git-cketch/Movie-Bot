from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎬 Фильмы"))
    return markup


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def sponsors_keyboard(sponsors):
    keyboard = InlineKeyboardMarkup()

    for sponsor in sponsors:
        link, _ = sponsor  # Разбираем кортеж
        if not link or not isinstance(link, str):  # Проверяем, что это строка
            continue
        username = link.lstrip('@')  # Убираем '@', если есть
        url = f"https://t.me/{username}"

        if " " in username or not username.isascii():  # Проверка на валидность
            continue

        keyboard.add(InlineKeyboardButton(f"Подписаться на @{username}", url=url))

    keyboard.add(InlineKeyboardButton("✅ Проверить подписку", callback_data="check_subs"))
    return keyboard




# Главное меню админа
def admin_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎬 Раздел Фильмы"))
    markup.add(KeyboardButton("📢 Раздел Спонсоры"))
    return markup

# Подменю "Фильмы"
def movies_admin_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("➕ Добавить фильм"))
    markup.add(KeyboardButton("✏ Изменить фильм"))
    markup.add(KeyboardButton("❌ Удалить фильм"))
    markup.add(KeyboardButton("🔙 Назад"))
    return markup

def sponsors_admin_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("➕ Добавить спонсора"))
    markup.add(KeyboardButton("✏ Изменить спонсора"))
    markup.add(KeyboardButton("❌ Удалить спонсора"))
    markup.add(KeyboardButton("🔙 Назад"))
    return markup