import telebot # библиотека telebot
from config import token # импорт токена
from telebot.types import Message
from telebot import TeleBot
bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Введите команду /help, чтобы узнать, как я работаю.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/start - начать работу с ботом\n/ban - забанить пользователя\n/unban - разбанить пользователя")


@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.reply_to_message:  # Проверка, что команда вызвана в ответ на сообщение
        chat_id = message.chat.id  # ID чата
        user_id = message.reply_to_message.from_user.id  # ID пользователя, которого разбанить
        chat = bot.get_chat(chat_id)  # Получение информации о чате

        try:
            # Проверяем тип чата
            if chat.type not in ['supergroup', 'channel']:
                bot.reply_to(message, "Команда доступна только в супергруппах или каналах.")
                return
            
            user_status = bot.get_chat_member(chat_id, user_id).status  # Статус пользователя в чате

            # Проверяем, что пользователь не администратор или создатель чата
            if user_status in ['administrator', 'creator']:
                bot.reply_to(message, "Невозможно разбанить администратора или создателя чата.")
            else:
                # Разбаниваем пользователя
                bot.unban_chat_member(chat_id, user_id)
                username = message.reply_to_message.from_user.username
                if username:
                    bot.reply_to(message, f"Пользователь @{username} был разбанен.")
                else:
                    bot.reply_to(message, "Пользователь был разбанен.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        bot.reply_to(message, "Команда должна быть выполнена в ответ на сообщение пользователя.")





@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")
@bot.message_handler(func=lambda message: True)
def echo_message(message: Message):
    if "https://" in message.text:
        user_id = message.from_user.id
        chat_id = message.chat.id

        # Получение статуса пользователя в чате
        user_status = bot.get_chat_member(chat_id, user_id).status

        # Проверка статуса пользователя
        if user_status not in ['administrator', 'creator']:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь был забанен за отправку ссылки.")

    # Отправка ответа с текстом сообщения
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message (message.chat.id, 'Привет новенький, я бот для управления чатом!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

bot.infinity_polling()