import random
import os

import openai

from db_func import addUserID_DB, delUserID_DB, selectUserID_DB, selectAdminID_DB, addAdminID_DB, selectAllUsers, addPhoneNumber, selectPhone, add_name, select_name, select_suc_select, user_suc_add, label_lines
from validator import normalize_text, check_number, check_number_ru, format_phone_number, log_error
from config import bot, OWNER_ID, telebot, NUMBERS_ROWS, MAIL
from telephone import postPhone
from mail_send import *

def count_lines_in_file(user_id : str) -> int:
    with open(f'users/{user_id}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return len(lines)

try:

    if not os.path.exists("users"):
        os.mkdir("users")

    with open('txt_files/prompt.txt', 'r', encoding='UTF-8') as prompt1:
        content_start = prompt1.read()

    openai.api_key = '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' # токен openai api ключ 


    print('----------------------------------------------------------------------')
    print(f"Промпт: {content_start}") 
    print('----------------------------------------------------------------------')

except Exception as e:
    log_error(e)

@bot.message_handler(commands=['start']) # изначалная проверка и запись в базу данных id пользователя
def command_start_checker(message : telebot.types.Message):
    try:
        if selectUserID_DB(message.from_user.id) == None:
            addUserID_DB(userID=message.from_user.id)
        bot.reply_to(message, f'👋🏻 Здравствуйте, ')

    except Exception as e:
        log_error(e)

@bot.message_handler(commands=['добавить'])
def handle_add_command(message: telebot.types.Message):
    if message.from_user.id != OWNER_ID:
        return
    # Получаем аргументы команды
    try:
        args = message.text.split()
        
        # Проверяем наличие аргументов
        if len(args) < 2:
            bot.reply_to(message, "Неверный формат команды. Используйте /добавить <id_пользователя>")
            return
        
        # Извлекаем id пользователя из аргументов
        user_id = args[1]
        user_suc_add(int(user_id))
        
        # Выполняем действия с полученным id пользователя (в данном случае просто отправляем сообщение)
        bot.send_message(message.chat.id, f"✅ Добавлен пользователь: `{user_id}`\n🔓Он сможет использовать бота", parse_mode='MarkdownV2')

    except Exception as e:
        log_error(e)

@bot.message_handler(commands=['рассылка'])
def command_posting_all(message: telebot.types.Message):
    if message.from_user.id != OWNER_ID:
        if select_suc_select(message.from_user.id) == None:
            return
    try:
        admin_id = message.from_user.id

        if selectAdminID_DB(admin_id) is not None or admin_id == OWNER_ID:
            bot.reply_to(message, "Выберите тип медиафайла: изображение, видео, аудио, текст или документ")
            bot.register_next_step_handler(message, get_media_type)

        else:
            bot.reply_to(message, "Вы не являетесь администратором")

    except Exception as e:
        log_error(e)


def get_media_type(message: telebot.types.Message):
    
    try:
        media_type = message.text.lower()    

        if media_type in ['изображение', 'видео', 'аудио', 'документ', 'текст']:
            bot.reply_to(message, f"Установите {media_type} для рассылки")
            bot.register_next_step_handler(message, get_media, media_type)

        else:
            bot.reply_to(message, "Неверный тип медиафайла. Выберите один из вариантов: изображение, видео, аудио, текст или документ")

    except Exception as e:
        log_error(e)


def get_media(message: telebot.types.Message, media_type: str):
    try:
        users_ids = selectAllUsers()
        print(media_type)
        print(message.audio)

        if media_type == 'изображение' and message.photo:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(f"media/images/image_{file_id}.jpg", 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"Установите текст для рассылки изображения")
            bot.register_next_step_handler(message, send_image, users_ids, file_id)

        elif media_type == 'видео' and message.video:
            file_id = message.video.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(f"media/videos/video_{file_id}.mp4", 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"Установите текст для рассылки видео")
            bot.register_next_step_handler(message, send_video, users_ids, file_id)

        elif media_type == 'аудио' and message.audio:
            
            file_id = message.audio.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(f"media/audio/audio_{file_id}.mp3", 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"Установите текст для рассылки аудио")
            bot.register_next_step_handler(message, send_audio, users_ids, file_id)

        elif media_type == 'текст' and message.text:

            text = message.text
            for user_id in users_ids:
                try:
                    bot.send_message(user_id, text)
                except: pass

            bot.reply_to(message, "✅ Отправка рассылки текста завершена")

        elif media_type == 'документ' and message.document:
            file_id = message.document.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(f"media/documents/document_{file_id}.pdf", 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"Установите текст для рассылки документа")
            bot.register_next_step_handler(message, send_document, users_ids, file_id)

        else:
            bot.reply_to(message, "Неверный тип медиафайла или отсутствует медиафайл для рассылки")

    except Exception as e:
        log_error(e)


def send_image(message: telebot.types.Message, users_ids, file_id):
    try:
        text = message.text
        for user_id in users_ids:
            with open(f"media/images/image_{file_id}.jpg", 'rb') as photo:
                try:
                    bot.send_photo(user_id, photo, caption=text)
                except: pass

        bot.reply_to(message, "✅ Отправка рассылки изображения завершена")
    except Exception as e:
        log_error(e)


def send_text(message: telebot.types.Message, users_ids):
    try:
        text = message.text
        for user_id in users_ids:
            try:
                bot.send_message(user_id, text)
            except: pass

        bot.reply_to(message, "✅ Отправка рассылки текста завершена")
    except Exception as e:
        log_error(e)


def send_video(message: telebot.types.Message, users_ids, file_id):
    try:
        text = message.text
        for user_id in users_ids:
            with open(f"media/videos/video_{file_id}.mp4", 'rb') as video:
                try:            
                    bot.send_video(user_id, video, caption=text)
                except: pass

        bot.reply_to(message, "✅ Отправка рассылки видео завершена")

    except Exception as e:
        log_error(e)


def send_audio(message: telebot.types.Message, users_ids, file_id):
    try:
        text = message.text
        for user_id in users_ids:
            with open(f"media/audio/audio_{file_id}.mp3", 'rb') as photo:
                try:
                    bot.send_audio(user_id, photo, caption=text)
                except: pass
    except Exception as e:
        log_error(e)

def send_document(message: telebot.types.Message, users_ids, file_id):
    try:
        text = message.text
        for user_id in users_ids:
            with open(f"media/documents/document_{file_id}.pdf", 'rb') as document:
                try:
                    bot.send_document(user_id, document, caption=text)
                except: pass

        bot.reply_to(message, "✅ Отправка рассылки документа завершена")

    except Exception as e:
        log_error(e)


def send_name(message : telebot.types.Message, user_id: int):
    print('Я в записи')
    name = message.text 
    add_name(user_id, name)
    bot.send_message(message.chat.id, f'Спасибо за ввод своего имени, {name}')
    return


@bot.message_handler(commands=['админ-добавить'])
def command_admin_add(message : telebot.types.Message):
    if message.from_user.id != OWNER_ID:
        if select_suc_select(message.from_user.id) == None:
            return
    try:
        if message.from_user.id == OWNER_ID:
            try:
                arg = message.text.split()[1:][0]
                arg = int(arg)
            except:
                bot.reply_to(message, "❌ ID должен содержать только цифры")
                return

            if selectAdminID_DB(message.from_user.id) != None:
                bot.reply_to(message, "❌ Такой администратор уже существует")
                return

            addAdminID_DB(arg)
            bot.reply_to(message, "✅ Администратор успешно добавлен")

        else:
            bot.reply_to(message, "❌ Вы не владелец бота")

    except Exception as e:
        log_error(e)

@bot.message_handler(commands=['мой-id'])
def command_my_id(message : telebot.types.Message):
    
    try:
        bot.reply_to(message, f"🆔 Ваш индентификатор: `{message.from_user.id}`", parse_mode='MarkdownV2')   
    except Exception as e:
        log_error(e)


@bot.message_handler()
def handle_message(message : telebot.types.Message):
    try:
        if format_phone_number(message.text):
            phone = format_phone_number(message.text)

        else: phone = message.text

        if check_number(phone) == True:

            if selectPhone(phone) == None:
                addPhoneNumber(phone)
            
                if check_number_ru(phone) == True:
                    postPhone(phone)

            sender = 'test1@akban.ru'
            subject = f'Сообщение из телеграм'
            file_path = f'users/{message.from_user.id}.txt'
            smtp_server = 'mail.akban.ru'       
            smtp_port = 465
            username = 'test1@akban.ru'
            password = '9hI@zzVbmP=k'
            name_telegram = message.from_user.full_name

            send_email_with_file_content(sender, MAIL, subject, file_path, smtp_server, smtp_port, username, password, name_telegram, selectPhone(phone), select_name(message.from_user.id))
            bot.reply_to(message, "🔉 Спасибо за ввод номера!")
            return
        
        else: pass

        randint = random.randint(0, 10)

        if randint == 1:
            number_phone_notify_text = "📞 Введите свой номер (по желанию)\n📀 Формат: +7 XXX XXX XX XX.\n🚩Можете ввести и другие номера так же в формате +XX XXX XXX XX XX или +X XXX XXX XX XX\n\n"

        elif randint != 1:
            number_phone_notify_text = ""
            
        if select_name(message.from_user.id) == None: 
            name = 'Пока не ввёл'
        else: 
            name = select_name(message.from_user.id)


        if f"{message.chat.id}.txt" not in os.listdir('users'):
            with open(f"users/{message.chat.id}.txt", "w+") as f:
                f.write('')

        with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as file:
            oldmes = file.read()

        if message.text == '/clear':
            with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as file:
                file.write('')
            return bot.send_message(chat_id=message.chat.id, text='История очищена!')

        send_message = bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста, подождите!')
        

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": oldmes},
                        {"role": "user","content": f'Предыдущие сообщения: {oldmes};Если видишь Бот:, не пиши об этом, это ты; Пользователя зовут: {name}; Запрос {content_start}: {message.text}'}], presence_penalty=0.6)
        

        generated_text = response.choices[0].message.content.strip()
        normalize = normalize_text(generated_text)
        bot.edit_message_text(text=f"{number_phone_notify_text} {normalize}", chat_id=message.chat.id, message_id=send_message.message_id)
        

        with open(f'users/{message.chat.id}.txt', 'a+', encoding='utf-8') as file:
            file.write(message.text.replace('\n', ' ') + '\n' + response.choices[0].message["content"].replace('\n', ' ') + '\n')


        with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) >= NUMBERS_ROWS +1:
            with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as f:
                f.writelines(lines[2:])


        if count_lines_in_file(str(message.from_user.id)) == 6 and select_name(message.from_user.id) == None:
            bot.send_message(message.chat.id, f'❗ Введите своё имя что бы мы могли обращаться к вам по нему')
            bot.register_next_step_handler(message, send_name, message.from_user.id)

        # label_lines(f'users/{message.chat.id}.txt')
        
    except Exception as e:
        log_error(e)

   

bot.polling()
