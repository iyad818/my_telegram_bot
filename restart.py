import os
import time
import subprocess

def start_bot():
    while True:
        # تشغيل ملف البوت
        process = subprocess.Popen(['python', 'bot.py'])

        # الانتظار حتى ينتهي تشغيل البوت
        process.communicate()

        # إذا توقف البوت، سيتم إعادة تشغيله بعد 5 ثواني
        print("Bot stopped, restarting...")
        time.sleep(5)

if __name__ == "__main__":
    start_bot()
