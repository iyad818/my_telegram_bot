import os
import time
import subprocess

def restart_bot():
    while True:
        try:
            # محاولة لتشغيل البوت
            subprocess.run(["python", "bot.py"], check=True)
        except subprocess.CalledProcessError:
            print("البوت توقف، محاولة إعادة تشغيله...")
            time.sleep(10)  # الانتظار 10 ثواني قبل المحاولة مرة أخرى

if __name__ == "__main__":
    restart_bot()
