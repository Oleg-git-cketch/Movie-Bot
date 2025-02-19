import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import init_db, add_movie_to_db, get_movie_by_code
from keyboard import main_menu, sponsors_keyboard

TOKEN = "7750734085:AAE4ezbZYWqDczqUujLntkV7H7HBI6nGjII"
ADMIN_ID = 7040733741  # Укажи свой Telegram ID
SPONSORS = ["@sigmaasd123"]  # Каналы, на которые нужно подписаться

bot = telebot.TeleBot(TOKEN)

init_db()

# Главное меню
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=main_menu())

# Обработка кнопки "Фильмы"
@bot.message_handler(func=lambda message: message.text == "🎬 Фильмы")
def show_sponsors(message):
    bot.send_message(message.chat.id, "Чтобы получить доступ к фильмам, подпишитесь на спонсоров:", reply_markup=sponsors_keyboard(SPONSORS))

# Проверка подписки
def check_subscription(user_id):
    for channel in SPONSORS:
        status = bot.get_chat_member(channel, user_id).status
        if status not in ['member', 'administrator', 'creator']:
            return False
    return True

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Вы подписаны! Введите код фильма:")
        bot.register_next_step_handler(call.message, get_movie)
    else:
        bot.send_message(call.message.chat.id, "❌ Вы не подписаны на все каналы! Подпишитесь и попробуйте снова.")

# Проверка кода и отправка фильма
def get_movie(message):
    movie_link = get_movie_by_code(message.text)
    if movie_link:
        bot.send_message(message.chat.id, f"🎬 Ваш фильм: {movie_link}")
    else:
        bot.send_message(message.chat.id, "❌ Код не найден. Попробуйте еще раз.")

# Админ-команда для добавления фильма
@bot.message_handler(commands=['add_movie'])
def add_movie(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Введите код фильма:")
        bot.register_next_step_handler(message, get_code)
    else:
        bot.send_message(message.chat.id, "❌ У вас нет прав доступа.")

def get_code(message):
    code = message.text
    bot.send_message(message.chat.id, "Теперь отправьте ссылку на фильм:")
    bot.register_next_step_handler(message, lambda msg: save_movie(msg, code))

def save_movie(message, code):
    add_movie_to_db(code, message.text)
    bot.send_message(message.chat.id, "✅ Фильм добавлен!")

# Запуск бота
bot.polling(none_stop=True)
