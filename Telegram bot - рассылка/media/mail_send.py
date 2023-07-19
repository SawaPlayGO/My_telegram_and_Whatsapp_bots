import smtplib
from email.message import EmailMessage

def send_email_with_file_content(sender, recipient, subject, file_path, smtp_server, smtp_port, username, password, name_telegram, number_phone, name_user):
    # Чтение содержимого файла
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # Очистка символов перевода строки и возврата каретки из subject
    subject = subject.replace('\n', '').replace('\r', '')

    # Формирование текста письма
    email_content = f"✈ Отправлено из: Телеграм\n📞 Номер телефона: {number_phone}\n🔎 Имя пользователя: {name_user}\n😊 Никнейм в телеграм: {name_telegram}\n📧 Контекст сообщения:\n\n{file_content}"

    try:
        # Установка соединения с SMTP-сервером
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # Аутентификация на сервере
            server.login(username, password)

            # Создание объекта письма
            msg = EmailMessage()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.set_content(email_content)

            # Отправка письма
            server.send_message(msg)
        print('Письмо с содержимым файла успешно отправлено!')
    except Exception as e:
        print(f'Ошибка при отправке письма: {e}')
