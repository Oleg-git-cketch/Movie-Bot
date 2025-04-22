import telebot
from telebot.types import ReplyKeyboardRemove
import os
from dotenv import load_dotenv
from db import (
    init_db, add_movie_to_db, get_movie_by_code, update_movie_in_db, delete_movie_from_db,
    add_sponsor_to_db, get_all_sponsors, update_sponsor_in_db, delete_sponsor_from_db
)
from keyboard import main_menu, sponsors_keyboard, movies_admin_menu, sponsors_admin_menu

load_dotenv()

TOKEN = os.getenv("7764598577:AAEe7_-nzbfyEkexT34O-qRn34P7jC5S-oI")

bot = telebot.TeleBot(TOKEN)
init_db()

def check_subscription(user_id):
    sponsors = get_all_sponsors()
    if not sponsors:
        return True

    for channel, is_mandatory in sponsors:
        if is_mandatory:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    if check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=main_menu())
    else:
        sponsors = get_all_sponsors()
        bot.send_message(message.chat.id, "Чтобы получить доступ к фильмам, подпишитесь на спонсоров:", reply_markup=sponsors_keyboard(sponsors))

@bot.message_handler(func=lambda message: message.text == "📢 Раздел Спонсоры")
def show_sponsors(message):
    sponsors = get_all_sponsors()
    bot.send_message(message.chat.id, "📢 Управление спонсорами:", reply_markup=sponsors_admin_menu())

@bot.message_handler(func=lambda message: message.text == "➕ Добавить спонсора")
def add_sponsor_start(message):
    bot.send_message(message.chat.id, "Отправьте ссылку на канал/группу:")
    bot.register_next_step_handler(message, get_sponsor_link)

def get_sponsor_link(message):
    link = message.text
    bot.send_message(message.chat.id, "Спонсор обязательный? (1 - Да, 0 - Нет)")
    bot.register_next_step_handler(message, lambda msg: save_sponsor(msg, link))

def save_sponsor(message, link):
    try:
        is_mandatory = int(message.text)
        if add_sponsor_to_db(link, is_mandatory):
            bot.send_message(message.chat.id, "✅ Спонсор добавлен!")
        else:
            bot.send_message(message.chat.id, "❌ Такой спонсор уже существует!")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите 1 (Да) или 0 (Нет). Попробуйте снова.")

@bot.message_handler(func=lambda message: message.text == "✏ Изменить спонсора")
def update_sponsor_start(message):
    bot.send_message(message.chat.id, "Введите текущую ссылку спонсора:")
    bot.register_next_step_handler(message, get_old_sponsor_link)

def get_old_sponsor_link(message):
    old_link = message.text
    bot.send_message(message.chat.id, "Введите новую ссылку спонсора:")
    bot.register_next_step_handler(message, lambda msg: get_new_sponsor_link(msg, old_link))

def get_new_sponsor_link(message, old_link):
    new_link = message.text
    bot.send_message(message.chat.id, "Спонсор обязательный? (1 - Да, 0 - Нет)")
    bot.register_next_step_handler(message, lambda msg: save_updated_sponsor(msg, old_link, new_link))

def save_updated_sponsor(message, old_link, new_link):
    try:
        is_mandatory = int(message.text)
        if update_sponsor_in_db(old_link, new_link, is_mandatory):
            bot.send_message(message.chat.id, "✅ Спонсор обновлен!")
        else:
            bot.send_message(message.chat.id, "❌ Спонсор не найден или ошибка обновления.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите 1 (Да) или 0 (Нет). Попробуйте снова.")

@bot.message_handler(func=lambda message: message.text == "❌ Удалить спонсора")
def delete_sponsor_start(message):
    bot.send_message(message.chat.id, "Введите ссылку спонсора для удаления:")
    bot.register_next_step_handler(message, delete_sponsor)

def delete_sponsor(message):
    link = message.text
    if delete_sponsor_from_db(link):
        bot.send_message(message.chat.id, "✅ Спонсор удален!")
    else:
        bot.send_message(message.chat.id, "❌ Спонсор не найден!")

@bot.message_handler(func=lambda message: message.text == "🎬 Фильмы")
def show_sponsors(message):
    if not check_subscription(message.from_user.id):
        sponsors = get_all_sponsors()
        bot.send_message(message.chat.id, "Чтобы получить доступ к фильмам, подпишитесь на спонсоров:", reply_markup=sponsors_keyboard(sponsors))
    else:
        bot.send_message(message.chat.id, "✅ Вы уже подписаны! Введите код фильма:")
        bot.register_next_step_handler(message, get_movie)

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id, "Введите код фильма:")
        bot.register_next_step_handler(call.message, get_movie)
    else:
        bot.send_message(call.message.chat.id, "❌ Вы не подписаны на все каналы! Подпишитесь и попробуйте снова.")

def get_movie(message):
    movie = get_movie_by_code(message.text)
    if movie:
        link, image_id, description = movie
        caption = f"🎬 *Фильм*: {message.text}\n\n📖 *Описание*: {description}\n\n🔗 [Смотреть фильм]({link})"
        bot.send_photo(message.chat.id, image_id, caption=caption, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ Код не найден. Попробуйте еще раз.")

@bot.message_handler(func=lambda message: message.text == "🎬 Раздел Фильмы")
def show_movies_admin_menu(message):
    bot.send_message(message.chat.id, "🎬 Управление фильмами:", reply_markup=movies_admin_menu())

@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_admin_menu(message):
    bot.send_message(message.chat.id, "Возвращение на главную...", reply_markup=main_menu())

bot.polling(none_stop=True)
