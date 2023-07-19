import sqlite3

conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE ads (
#     user_id TEXT,
#     title TEXT,
#     description TEXT,
#     city TEXT
# )
# ''')

def add_AD(user_id: str, title: str, description : str, city : str):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO ads (user_id, title, description, city) VALUES (?, ?, ?, ?)", (str(user_id), str(title), str(description), str(city)))
    conn.commit()

def select_AD(city: str) -> tuple:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Выполнение запроса SELECT с условием WHERE
    cursor.execute("SELECT user_id, title, description, city FROM ads WHERE city = ?", (str(city),))

    # Получение результатов запроса
    try:
        ads = cursor.fetchone()
        return tuple(ads)
    except:
        return None