import subprocess
import time
from config import HOURS

while True:
    # Запускаем bot.py в отдельном процессе
    process = subprocess.Popen(['python', 'bot.py'])

    # Ожидаем
    time.sleep(HOURS * 3600) # каждые пять секунд

    # Останавливаем выполнение процесса bot.py
    process.terminate()
