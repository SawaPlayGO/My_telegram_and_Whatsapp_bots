import sqlite3
from config import telebot, bot, CHAT_GROUP_ID
import ast
import time
import threading
import traceback
import datetime
import pytz



conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE users (
#     user_id INTEGER
# )
# ''')

# cursor.execute('''
# CREATE TABLE posts (
#     message_text TEXT,
#     first_name TEXT,
#     content_type TEXT,
#     message_id TEX         
# )
# ''')

# cursor.execute('''
# CREATE TABLE timers (
#     user_id TEXT  
# )
# ''')

# cursor.execute('''
# CREATE TABLE capcha (
#     user_id TEXT,
#     message_id TEXT,
#     answer TEXT
# )
# ''')

# cursor.execute('''
# CREATE TABLE dontcapha (
#     user_id TEXT
# )
# ''')

def addUserID_DB(userID : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (user_id) VALUES (?)", (userID,))
    conn.commit()

def delUserID_DB(userID : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE user_id=?", (userID,))
    conn.commit()

def selectUserID_DB(userID : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (userID,))

    # Получение результатов запроса
    try:
        user = cursor.fetchone()
        return int(user[0])
    except:
        return None
    

def selectAllUsers() -> list:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    # Выполнение запроса SELECT для извлечения всех user_id
    cursor.execute("SELECT user_id FROM users")

    # Получение результатов запроса
    rows = cursor.fetchall()

    # Создание списка user_id
    user_ids = [row[0] for row in rows]

    # Вывод списка user_id
    return user_ids


def selectAdminID_DB(adminID : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT admin_id FROM admins WHERE admin_id = ?", (adminID,))

    # Получение результатов запроса
    row = cursor.fetchone()

    try:
        admin = cursor.fetchone()
        return int(admin[0])
    except:
        return None
    

def addAdminID_DB(adminID : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO admins (admin_id) VALUES (?)", (adminID,))
    conn.commit()


def addPostID_DB(text : str, first_name : str, content_type : str, message_id : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO posts (message_text, first_name, content_type, message_id) VALUES (?, ?, ?, ?)", (str(text), str(first_name), str(content_type), str(message_id),))
    conn.commit()

def delPostID_DB(message_id : telebot.types.Message):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM posts WHERE message_id=?", (str(message_id),))
    conn.commit()
    

def selectPostID_DB(message_id : telebot.types.Message):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    l = []
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT message_text FROM posts WHERE message_id = ?", (str(message_id),))

    # Получение результатов запроса
    try:
        user = cursor.fetchone()
        user = user[0]
        l.append(user)
    except:
        return None
    


    cursor.execute("SELECT content_type FROM posts WHERE message_id = ?", (str(message_id),))

    # Получение результатов запроса
    try:
        user = cursor.fetchone()
        user = user[0]
        l.append(user)
    except:
        return None
    


    cursor.execute("SELECT first_name FROM posts WHERE message_id = ?", (str(message_id),))

    # Получение результатов запроса
    try:
        user = cursor.fetchone()
        user = user[0]
        l.append(user)
    except:
        return None
    print(l)
    return l
    

def selectPost1ID_DB(message_id : str):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute(f"SELECT message FROM posts WHERE message LIKE '%{message_id}%'")

    # Получение результатов запроса
    user = cursor.fetchone()
    user = (str(user[0]))
    data = ast.literal_eval(user)
    data = telebot.types.Message()
    return data

def delPostID_DB(message_id : str):

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    # Выполнение запроса к базе данных для удаления ячеек
    cursor.execute("DELETE FROM posts WHERE message_id=?", (str(message_id), ))

    # Сохранение изменений в базе данных
    conn.commit()

def addtimer_DB(user_id):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO timers (user_id) VALUES (?)", (str(user_id),))
    conn.commit()

def deltimer_DB(user_id : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM timers WHERE user_id=?", (str(user_id),))
    conn.commit()
    

def selecttimer_DB(user_id : int) -> int:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT user_id FROM timers WHERE user_id = ?", (str(user_id),))

    try:
        user = cursor.fetchone()
        user = user[0]
        return int(user)
    except:
        return None
    
def select_capha_timer(user_id : int) -> tuple:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT user_id, message_id, answer FROM capcha WHERE user_id = ?", (str(user_id),))

    try:
        user = cursor.fetchone()
        return user
    except:
        return None
    

def add_capha_timer(user_id, message_id, answer):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO capcha (user_id, message_id, answer) VALUES (?, ?, ?)", (str(user_id), str(message_id), str(answer)))
    conn.commit()

def del_capcha_timer(user_id : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM capcha WHERE user_id=?", (str(user_id),))
    conn.commit()

# =================================================================================================================================

def potoc_ne_reshil_caphu(user_id):
    timer_thread = threading.Thread(target=start_potoc_yesli_ne_reshil_caphu, args=(user_id,))
    timer_thread.start()

    add_timer_yesli_ne_reshil_caphu(user_id)

def start_potoc_yesli_ne_reshil_caphu(user_id):
    time.sleep(3600)
    del_capcha_timer_yesli_ne_reshil_caphu(user_id)
    bot.send_message(CHAT_GROUP_ID, "✅ Вы можете снова пройти капчу")
    

def select_capha_yesli_ne_reshil_caphu(user_id : int) -> int:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT user_id FROM dontcapha WHERE user_id = ?", (str(user_id),))

    try:
        user = cursor.fetchone()
        user = int(user[0])
        return user
    except:
        return None
    

def add_timer_yesli_ne_reshil_caphu(user_id):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO dontcapha (user_id) VALUES (?)", (str(user_id),))
    conn.commit()

def del_capcha_timer_yesli_ne_reshil_caphu(user_id : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM dontcapha WHERE user_id=?", (str(user_id),))
    conn.commit()

# ==============================================================================================================================

def add_potoc_timer(user_id):
    # Проверяем, существует ли уже таймер для данного пользователя
    if selecttimer_DB(user_id) != None:
        bot.send_message(CHAT_GROUP_ID, 'Слишком рано, ожидайте.')
    else:
        # Создаем отдельный поток с таймером для данного пользователя
        timer_thread = threading.Thread(target=wait_and_send_message_timer, args=(user_id,))
        timer_thread.start()
        # Сохраняем поток в словаре user_timers
        addtimer_DB(user_id)

def wait_and_send_message_timer(user_id):
    time.sleep(10)  # Ожидаем 10 секунд
    # Время вышло, отправляем сообщение пользователю
    bot.send_message(CHAT_GROUP_ID, 'Всё окей, можно писать')
    # Удаляем таймер из словаря после отправки сообщения
    deltimer_DB(user_id)

# =============================================================================================================================

def add_potoc_capcha(user_id, message_id, answer):
    # Создаем отдельный поток с таймером для данного пользователя
    timer_thread = threading.Thread(target=capcha_waiting, args=(user_id, message_id, answer))
    timer_thread.start()
    # Сохраняем поток в словаре user_timers
    add_capha_timer(user_id, message_id, answer)

def capcha_waiting(user_id, message_id, answer):
    time.sleep(120) # Ожидаем 120 секунд
    if select_capha_timer(user_id) == None:
        return

    else:
        # Время вышло, отправляем сообщение пользователю
        # bot.send_message(CHAT_GROUP_ID, 'Вы не успели, решить капчу заявка на вступление отклонена. Повторно пройти капчу можо будет через час.')
        try:
            bot.delete_message(CHAT_GROUP_ID, int(message_id))
        except:
            pass
        # Удаляем таймер из словаря после отправки сообщения
        del_capcha_timer(user_id)
        # bot.decline_chat_join_request(CHAT_GROUP_ID, int(user_id))
        potoc_ne_reshil_caphu(user_id)

# =============================================================================================================================
def log_error(error):
    error_message = traceback.format_exc()

    # Установка временной зоны для Москвы
    moscow_tz = pytz.timezone('Europe/Moscow')

    # Получение текущего времени в Москве
    current_time = datetime.datetime.now(tz=moscow_tz)

    # Форматирование времени
    formatted_time = current_time.strftime('%d.%m.%Y | %H:%M:%S')

    with open("error.txt", "a", encoding="utf-8") as file:
        file.write(f"{formatted_time}\n")
        file.write("Ошибка:\n")
        file.write(str(error) + "\n")
        file.write("Traceback:\n")
        file.write(error_message + "\n")
        file.write("-----------------\n")