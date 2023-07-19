import re

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