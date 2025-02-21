import telebot
from db import (
    init_db, add_movie_to_db, get_movie_by_code, update_movie_in_db, delete_movie_from_db,
    add_sponsor_to_db, get_all_sponsors, update_sponsor_in_db, delete_sponsor_from_db
)
from keyboard import main_menu, sponsors_keyboard, movies_admin_menu, sponsors_admin_menu, admin_menu

TOKEN = "7764598577:AAEe7_-nzbfyEkexT34O-qRn34P7jC5S-oI"
ADMIN_ID = 7040733741  # Укажи свой Telegram ID

bot = telebot.TeleBot(TOKEN)
init_db()

@bot.message_handler(commands=['start'])
def start(message):
    sponsors = get_all_sponsors()
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=main_menu())
    if sponsors:
        bot.send_message(message.chat.id, "Чтобы получить доступ к фильмам, подпишитесь на спонсоров:", reply_markup=sponsors_keyboard(sponsors))

@bot.message_handler(func=lambda message: message.text == "🎬 Фильмы")
def show_sponsors(message):
    sponsors = get_all_sponsors()
    bot.send_message(message.chat.id, "Чтобы получить доступ к фильмам, подпишитесь на спонсоров:", reply_markup=sponsors_keyboard(sponsors))

def check_subscription(user_id):
    sponsors = get_all_sponsors()
    for channel in sponsors:
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

def get_movie(message):
    movie = get_movie_by_code(message.text)
    if movie:
        link, image_id, description = movie
        caption = f"🎬 *Фильм*: {message.text}\n\n📖 *Описание*: {description}\n\n🔗 [Смотреть фильм]({link})"
        bot.send_photo(message.chat.id, image_id, caption=caption, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ Код не найден. Попробуйте еще раз.")

def is_admin(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "👮‍♂️ Админ панель:", reply_markup=admin_menu())
    else:
        bot.send_message(message.chat.id, "❌ У вас нет прав доступа.")

@bot.message_handler(func=lambda message: message.text == "➕ Добавить фильм")
def add_movie_start(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "Отправьте постер фильма (фото).")
        bot.register_next_step_handler(message, get_movie_photo)

def get_movie_photo(message):
    if not message.photo:
        bot.send_message(message.chat.id, "❌ Это не фото! Попробуйте еще раз.")
        return
    image_id = message.photo[-1].file_id
    bot.send_message(message.chat.id, "Теперь введите код фильма:")
    bot.register_next_step_handler(message, lambda msg: get_movie_code(msg, image_id))

def get_movie_code(message, image_id):
    code = message.text
    bot.send_message(message.chat.id, "Теперь отправьте ссылку на фильм:")
    bot.register_next_step_handler(message, lambda msg: get_movie_link(msg, code, image_id))

def get_movie_link(message, code, image_id):
    link = message.text
    bot.send_message(message.chat.id, "Теперь отправьте описание фильма:")
    bot.register_next_step_handler(message, lambda msg: save_movie(msg, code, link, image_id))

def save_movie(message, code, link, image_id):
    description = message.text
    if add_movie_to_db(code, link, image_id, description):
        bot.send_message(message.chat.id, "✅ Фильм добавлен!")
    else:
        bot.send_message(message.chat.id, "❌ Фильм с таким кодом уже существует!")

@bot.message_handler(func=lambda message: message.text == "🎬 Раздел Фильмы")
def show_movies_admin_menu(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "🎬 Управление фильмами:", reply_markup=movies_admin_menu())
    else:
        bot.send_message(message.chat.id, "❌ У вас нет прав доступа.")


bot.polling(none_stop=True)
