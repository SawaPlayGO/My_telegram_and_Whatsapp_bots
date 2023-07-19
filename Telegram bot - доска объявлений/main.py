from config import bot, telebot
from database import *


keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
search = telebot.types.KeyboardButton('📢 Создать объявление')
addAD = telebot.types.KeyboardButton('🔎 Поиск объявлений')
keyboard.add(search, addAD)


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):

    # Получаем id пользователя: user_id
    # Получаем id чата: chat_id
    # Получаем имя пользователя: name_user
    user_id = message.from_user.id
    name_user = message.from_user.first_name
    chat_id = message.chat.id

    bot.send_message(chat_id, f'''
👋🏻 Привет {name_user}, добро пожаловать на нашу доску объявлений.

🏅 Наши преимущества:

1️⃣ - Ищи нужные тебе услуги
2️⃣ - Создай объявление и прорекламируй свои услуги для людей, которым они нужны.
3️⃣ - Хорошие фильтры и поиск по городу.

🟥 Для начала поиска или размещения объявления нажмите соответствующую кнопку.
''', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == '🔎 Поиск объявлений')
def step1_search(message: telebot.types.Message):

    searching_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    moscow = telebot.types.KeyboardButton('Москва')
    spb = telebot.types.KeyboardButton('Санкт-Питербург')
    searching_keyboard.add(moscow, spb)

    bot.send_message(message.chat.id, '1️⃣ Выберите город', reply_markup=searching_keyboard)
    bot.register_next_step_handler(message, step2_search,)

def step2_search(message: telebot.types.Message):
    city = message.text

    if city == 'Москва':
        city_searh = select_AD(city=city)
        print(1)
        print(city_searh)
        if city_searh != None:
            if city_searh[3] == 'Москва':
                bot.send_message(int(city_searh[0]), f'🏡 Объявление в: *{city}*\nНазваине: *{city_searh[1]}*\nОписание: *{city_searh[2]}*', parse_mode="Markdown", reply_markup=keyboard)
                return
        else:
            bot.send_message(int(city_searh[0]), f'Объявление в *{city}* не найдено', reply_markup=keyboard, parse_mode="Markdown")
            return
    else:
        bot.send_message(int(city_searh[0]), f'Объявление в *{city}* не найдено', reply_markup=keyboard, parse_mode="Markdown")
        return



@bot.message_handler(func=lambda message: message.text == '📢 Создать объявление')
def step1(message: telebot.types.Message):
    bot.send_message(message.chat.id, '1️⃣ Введите название вашего объявления')
    bot.register_next_step_handler(message, step_createAD_1)

def step_createAD_1(message: telebot.types.Message):
    message_text = message.text
    bot.send_message(message.chat.id, '2️⃣ Введите город, где оказывается данная услуга')
    bot.register_next_step_handler(message, step_createAD_2, message_text)

def step_createAD_2(message: telebot.types.Message, message_text):
    city = message.text
    bot.send_message(message.chat.id, '3️⃣ Введите описание вашего объявления')
    bot.register_next_step_handler(message, step_createAD_3, message_text, city)

def step_createAD_3(message: telebot.types.Message, message_text, city):
    ad_description = message.text

    post_ad = telebot.types.ReplyKeyboardMarkup(row_width=1)
    yes = telebot.types.KeyboardButton('✅ Да')
    no = telebot.types.KeyboardButton('❌ Нет')
    back = telebot.types.KeyboardButton('⏮ Назад')
    post_ad.add(yes, no, back)

    bot.send_message(message.chat.id, 'Мы опубликуем ваше объявление?', reply_markup=post_ad)
    bot.register_next_step_handler(message, step_createAD_4, message_text, city, ad_description)

def step_createAD_4(message: telebot.types.Message, message_text, city, ad_description):
    if message.text == '✅ Да':
        bot.send_message(message.chat.id, '✅ Ваше объявление опубликовано. Вот как оно выглядит: ')
        bot.send_message(message.chat.id, f'Город: {city}\nНазвание: {message_text}\n\nОписание: {ad_description}', reply_markup=keyboard)
        add_AD(user_id=message.from_user.id, title=message_text, description=ad_description, city=city)
        
    elif message.text == '❌ Нет':
        bot.send_message(message.chat.id, 'Хорошо, ваше объявление не опубликовано.', reply_markup=keyboard)
    elif message.text == '⏮ Назад':
        bot.send_message(message.chat.id, 'Выберите что ещё хотите сделать', reply_markup=keyboard)

bot.infinity_polling()






