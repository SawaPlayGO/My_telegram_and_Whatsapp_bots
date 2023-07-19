import random
import os
import openai

from validator import normalize_text, format_phone_number, check_number, check_number_ru, log_error
from config import bot, Notification, OWNER_NUMBER, NUMBERS_ROWS
from db_func import selectAdminID_DB, selectAllUsers, selectUserID_DB, addUserID_DB, selectPhone, addPhoneNumber
from telephone import postPhone

try:
    openai.api_key = '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'

    with open('txt_files/prompt.txt', 'r', encoding='UTF-8') as prompt1:
        content_start = prompt1.read()

        print(content_start)
except Exception as e:
    log_error(e)

@bot.router.message()
def message_handler(notification: Notification) -> None:

    global content_start
    try:
        if selectUserID_DB(str(notification.get_sender())) == None:
            addUserID_DB(notification.get_sender())

            print(f"Юзер id: {notification.get_sender()}")
            print(f"Чат id: {notification.get_chat()}")
            

        if format_phone_number(notification.message_text):
            phone = format_phone_number(notification.message_text)


        else: phone = notification.message_text

        if check_number(phone) == True:

            if selectPhone(phone) == None:
                addPhoneNumber(phone)
            
                if check_number_ru(phone) == True:
                    postPhone(phone)
            return
        else: pass

        if notification.message_text == "/мой-id":
            notification.answer(f"Ваш индентефикатор: {notification.get_sender()}")
            return
        
        if notification.message_text.startswith("/рассылка"):
            if notification.get_sender() == OWNER_NUMBER:
                # Найдите позицию первого пробела в сообщении
                space_index = notification.message_text.find(' ')

                # Извлеките текст после команды "/рассылка"
                text = notification.message_text[space_index+1:]
                # Ваш код обработки первой строки
                allUsers = selectAllUsers()

                for user in allUsers:
                        bot.api.sending.sendMessage(user, text)
                return
            
        randint = random.randint(0, 1)
        print(randint)

        if randint == 1:
            number_phone_notify_text = ""

        elif randint != 1:
            number_phone_notify_text = ""

        if f"{notification.get_sender()}.txt" not in os.listdir('users'):
            with open(f"users/{notification.get_sender()}.txt", "x") as f:
                f.write('')

        with open(f'users/{notification.get_sender()}.txt', 'r', encoding='utf-8') as file:
            oldmes = file.read()

        if notification.message_text == '/clear':
            with open(f'users/{notification.chat.id}.txt', 'w', encoding='utf-8') as file:
                file.write('')
            return notification.answer(message='История очищена!')

        notification.answer(message='Обрабатываю запрос, пожалуйста, подождите!')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": oldmes},
                        {"role": "user","content": f'Предыдущие сообщения: {oldmes}; Запрос {content_start}: {notification.message_text}'}], presence_penalty=0.6)
        

        generated_text = response.choices[0].message.content.strip()
        normalize = normalize_text(generated_text)
        notification.answer(message=f"{number_phone_notify_text} {normalize}")

        with open(f'users/{notification.get_sender()}.txt', 'a+', encoding='utf-8') as file:
            file.write(notification.message_text.replace('\n', ' ') + '\n' + response.choices[0].message["content"].replace('\n', ' ') + '\n')


        with open(f'users/{notification.get_sender()}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) >= NUMBERS_ROWS +1:
            with open(f'users/{notification.get_sender()}.txt', 'w', encoding='utf-8') as f:
                f.writelines(lines[2:])

    except Exception as e:
        log_error(e)


bot.run_forever()