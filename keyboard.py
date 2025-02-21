from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎬 Фильмы"))
    return markup

def sponsors_keyboard(sponsors):
    markup = InlineKeyboardMarkup()
    for channel in sponsors:
        markup.add(InlineKeyboardButton(f"Подписаться на {channel}", url=channel))  # Используем ссылку как есть
    markup.add(InlineKeyboardButton("✅ Проверить подписку", callback_data="check_subs"))
    return markup


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