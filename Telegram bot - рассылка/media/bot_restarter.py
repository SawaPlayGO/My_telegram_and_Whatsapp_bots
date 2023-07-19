import subprocess
import schedule
import time

# Пусть к файлу `bot.py` в той же директории
BOT_FILE_PATH = 'bot.py'

def restart_bot():
    # Завершаем предыдущий процесс бота, если он запущен
    stop_bot()

    # Запускаем новый процесс `bot.py`
    start_bot()

def start_bot():
    # Запускаем `bot.py` в новом процессе
    subprocess.Popen(['python', BOT_FILE_PATH])

def stop_bot():
    # Завершаем все процессы с именем `bot.py`
    subprocess.call(['pkill', '-f', BOT_FILE_PATH])

if __name__ == '__main__':
    # Планируем перезапуск каждую минуту
    schedule.every().minute.do(restart_bot)

    while True:
        # Запускаем отложенные задачи
        schedule.run_pending()
        time.sleep(1)
