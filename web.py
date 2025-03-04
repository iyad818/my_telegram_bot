import os
import threading
import time
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

# متغيرات لتخزين حالة البوت وعملية التشغيل
bot_running = False
bot_process = None

def start_bot():
    """ تشغيل البوت في مسار مستقل """
    global bot_running, bot_process
    if not bot_running:
        bot_process = subprocess.Popen(["python3", "bot.py"])
        bot_running = True

def check_bot_status():
    """ التحقق مما إذا كان البوت لا يزال قيد التشغيل """
    global bot_running
    if bot_process and bot_process.poll() is not None:  # إذا كان البوت متوقفًا
        bot_running = False

@app.route('/')
def home():
    """ عرض حالة البوت """
    check_bot_status()
    return jsonify({"bot_status": "Running" if bot_running else "Stopped"})

def run_flask():
    """ تشغيل Flask على المنفذ 8000 """
    app.run(host='0.0.0.0', port=8000)

# تشغيل Flask في مسار منفصل
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# تشغيل البوت عند بدء التشغيل
start_bot()

# التحقق من حالة البوت كل 10 ثوانٍ وإعادة تشغيله إذا لزم الأمر
while True:
    check_bot_status()
    if not bot_running:
        print("⚠️ البوت توقف! إعادة تشغيله...")
        start_bot()
    time.sleep(10)
