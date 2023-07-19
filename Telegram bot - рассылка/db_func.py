import sqlite3
from validator import check_number


conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE users (
#     user_id INTEGER
# )
# ''')

# cursor.execute('''
# CREATE TABLE admins (
#     admin_id INTEGER
# )
# ''')

# cursor.execute('''
# CREATE TABLE phones (
#     number_phone TEXT
# )
# ''')

# cursor.execute('''
# CREATE TABLE users_names (
#     user_id TEXT,
#     name TEXT
# )
# ''')

# cursor.execute('''
# CREATE TABLE users_suc (
#     user_id TEXT
# )
# ''')

def user_suc_add(user_id : int):

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users_suc (user_id) VALUES (?)", (user_id,))
    conn.commit()

def select_suc_select(user_id : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT user_id FROM users_suc WHERE user_id = ?", (user_id,))

    # Получение результатов запроса
    try:
        user = cursor.fetchone()
        return int(user[0])
    except:
        return None

def add_name(user_id: int, name: str) -> None:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users_names (user_id, name) VALUES (?, ?)", (str(user_id), name))
    conn.commit()

def select_name(user_id: int) -> str:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT name FROM users_names WHERE user_id = ?", (user_id,))

    # Получение результатов запроса
    try:
        name = cursor.fetchone()
        return str(name[0])
    except:
        return None
    

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


def addPhoneNumber(phon_number : str):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO phones (number_phone) VALUES (?)", (phon_number,))
    conn.commit()


def selectPhone(phon_number : int):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT number_phone FROM phones WHERE number_phone = ?", (phon_number,))

    try:
        phone = cursor.fetchone()
        print(phone)
        return str(phone[0])
    except:
        return None
    

def label_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    labeled_lines = []
    for index, line in enumerate(lines, 1):
        if index % 2 == 1:
            labeled_lines.append(f"Пользователь: {line.strip()}\n")
        elif line.startswith("Бот:"):
            labeled_lines.append(line)
        else:
            labeled_lines.append(f"Бот: {line.strip()}\n")

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(''.join(labeled_lines))
