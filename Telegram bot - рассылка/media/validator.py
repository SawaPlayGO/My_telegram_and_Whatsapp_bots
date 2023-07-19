import re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import traceback
import datetime
import pytz


def normalize_text(text):
    # Удаление символов перевода строки и пробелов в начале и конце строки
    text = text.strip()
    # Замена последовательностей символов перевода строки на пробел
    text = re.sub(r'\n+', ' ', text)
    # Замена повторяющихся пробелов на один пробел
    text = re.sub(r'\s+', ' ', text)
    # Удаление специальных символов и управляющих последовательностей
    text = re.sub(r'[^\w\s.,?!]', '', text)
    # Замена многоточия на одну точку
    text = re.sub(r'\.{2,}', '.', text)
    # Удаление пробелов перед знаками препинания
    text = re.sub(r'\s+([.,?!])', r'\1', text)
    # Приведение первой буквы каждого предложения к заглавной
    text = '. '.join(sentence.capitalize() for sentence in text.split('. '))

    return text

import re

def check_number_ru(phone_number : str) -> bool:
    result = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', phone_number)
    return bool(result)

def check_number(phone_number : str) -> bool:

    try:
        number = phone_number
        check = carrier._is_mobile(number_type(phonenumbers.parse(number)))
        return check
    except:
        return None


def format_phone_number(phone_number):
    # Удалить все символы, кроме цифр
    phone_number = ''.join(filter(str.isdigit, phone_number))

    # Проверить формат номера телефона
    if phone_number.startswith('8'):
        if len(phone_number) == 11:
            phone_number = '+7' + phone_number[1:]
        else:
            return None
    elif phone_number.startswith('9'):
        if len(phone_number) == 10:
            phone_number = '+7' + phone_number
        else:
            return None
    elif phone_number.startswith('7'):
        if len(phone_number) == 11:
            phone_number = '+7' + phone_number[1:]
        else:
            return None
    else:
        return None

    return phone_number


def log_error(error):
    error_message = traceback.format_exc()

    # Установка временной зоны для Москвы
    moscow_tz = pytz.timezone('Europe/Moscow')

    # Получение текущего времени в Москве
    current_time = datetime.datetime.now(tz=moscow_tz)

    # Форматирование времени
    formatted_time = current_time.strftime('%d.%m.%Y | %H:%M:%S')

    with open("txt_files/error.txt", "a", encoding="utf-8") as file:
        file.write(f"{formatted_time}\n")
        file.write("Ошибка:\n")
        file.write(str(error) + "\n")
        file.write("Traceback:\n")
        file.write(error_message + "\n")
        file.write("-----------------\n")
