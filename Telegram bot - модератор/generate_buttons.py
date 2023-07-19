import random
from config import telebot, bot, CHAT_GROUP_ID
from db_func import *


types = telebot.types

smile_dict = {
    0 : "🍎",
    1 : '🍐',
    2 : '🍒',
    3 : '🍇',
    4 : '🍌',
    5 : '🥑',
    6 : '🍍',
    7 : '🍊',
    8 : '🥝',
    9 : '🍋',
    10 : '🍓',
}

def generate_random_button(amount: int, message: types.Message, text: str) -> list:
    random_nums = random.sample(range(9), amount)
    markup = types.InlineKeyboardMarkup()
    for random_num in random_nums:
        fruct = smile_dict[random_num]
        button = types.InlineKeyboardButton(fruct, callback_data=str(random_num))
        markup.add(button)

    answer = str(random.choice(random_nums))
    answer_fruct = smile_dict[int(answer)]
    mess = bot.send_message(CHAT_GROUP_ID, f"{text}, {answer_fruct}", reply_markup=markup)

    add_potoc_capcha(int(message.from_user.id), int(mess.message_id), int(answer))

