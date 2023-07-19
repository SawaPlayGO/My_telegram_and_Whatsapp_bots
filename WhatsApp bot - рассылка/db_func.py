import sqlite3
from validator import check_number


conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE users (
#     user_id TXT
# )
# ''')

# cursor.execute('''
# CREATE TABLE phones (
#     number_phone TEXT
# )
# ''')




def addUserID_DB(userID : str):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (user_id) VALUES (?)", (userID,))
    conn.commit()

def delUserID_DB(userID : str):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE user_id=?", (userID,))
    conn.commit()

def selectUserID_DB(userID : str):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (userID,))

    # Получение результатов запроса
    try:
        user = cursor.fetchone()
        return str(user[0])
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
    