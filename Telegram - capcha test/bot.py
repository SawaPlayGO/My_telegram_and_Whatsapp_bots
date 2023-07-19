import telebot
from pyTelegramBotCAPTCHA import CaptchaManager, CaptchaOptions

bot = telebot.TeleBot("6086212674:AAGoWZEl7q8eqn3wyvhWwXxoFwCvW5Im4lc")

options = CaptchaOptions()
options.generator = "default"  # Use the default generator

captcha_manager = CaptchaManager(bot.get_me().id, default_options=options)

import telebot
from telebot.types import Message

# Вставьте ваш токен Telegram-бота
TOKEN = '6086212674:AAGoWZEl7q8eqn3wyvhWwXxoFwCvW5Im4lc'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['new_chat_members'])
def welcome_message(message: Message):

    global user, chat_id

    user = message.new_chat_members[0]
    chat_id = message.chat.id

    captcha_manager.send_new_captcha(bot, message.chat, message.from_user)


# Callback query handler
@bot.callback_query_handler(func=lambda callback: True)
def on_callback(callback):
    captcha_manager.update_captcha(bot, callback)


# Handler for correct solved CAPTCHAs
@captcha_manager.on_captcha_correct
def on_correct(captcha):
    bot.send_message(captcha.chat.id, f"Добро пожаловать.")
    captcha_manager.delete_captcha(bot, captcha)


# Handler for wrong solved CAPTCHAs
@captcha_manager.on_captcha_not_correct
def on_not_correct(captcha):
    bot.send_message(captcha.chat.id, f"❌ : Вы не прошли капчу.")
    captcha_manager.delete_captcha(bot, captcha)
    
    bot.ban_chat_member(chat_id, user.id)

    


# Handler for timed out CAPTCHAS
@captcha_manager.on_captcha_timeout
def on_timeout(captcha):
    bot.send_message(captcha.chat.id, f"❌ : You did not solve the CAPTCHA!")
    captcha_manager.delete_captcha(bot, captcha)


    # Отправляем приветственное сообщение

bot.polling()
