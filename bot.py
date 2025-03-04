#$
import requests
import string
import telebot
import os
import random
import json
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from faker import Faker
from telebot import types
from telebot.types import LabeledPrice, PreCheckoutQuery
from datetime import datetime, timedelta


TOKEN = "7312710877:AAGgO0DlOSwOhOfDKZganTkbgN2dJX-hB6Y"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # يحصل على مسار مجلد السكريبت الرئيسي
API_URL = "https://lookup.binlist.net"
USER_LAST_BIN_REQUEST = {}
ADMINS = [7192243354, 987654321] 
VIP_FILE = os.path.join(BASE_DIR, "vip_data.json")
subscription_data = VIP_FILE
vip_data = VIP_FILE
TOP_BIN_FILE = os.path.join(BASE_DIR, "top_bin.json")
FLAGS_FILE = os.path.join(BASE_DIR, "flags.json")
CODES_FILE = os.path.join(BASE_DIR, "codes.json")
data_file = os.path.join(BASE_DIR, "data.json")
gad_file = os.path.join(BASE_DIR, "gad.json")
IMAGES_FOLDER = os.path.join(BASE_DIR, "images")
IMAGE_PATH = IMAGES_FOLDER

image_list = []
if os.path.exists(IMAGES_FOLDER):
    image_list = [os.path.join(IMAGES_FOLDER, img) for img in os.listdir(IMAGES_FOLDER) if img.endswith(('png', 'jpg', 'jpeg'))]
image_index = 0

def luhn_generate(bin_prefix):
    cc_number = [int(d) for d in bin_prefix]
    while len(cc_number) < 15:
        cc_number.append(random.randint(0, 9))
    sum_ = 0
    for i in range(14, -1, -1):
        digit = cc_number[i]
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_ += digit
    last_digit = (10 - (sum_ % 10)) % 10
    cc_number.append(last_digit)
    return "".join(map(str, cc_number))

def luhn_check(card_number):
    digits = [int(d) for d in card_number]
    checksum = 0
    is_second = False
    for i in range(len(digits) - 1, -1, -1):
        d = digits[i]
        if is_second:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
        is_second = not is_second
    return checksum % 10 == 0
def get_random_image():
    """إرجاع صورة عشوائية من المجلد المحدد"""
    if not os.path.exists(IMAGE_PATH):
        return None
    images = [f for f in os.listdir(IMAGE_PATH) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not images:
        return None
    return os.path.join(IMAGE_PATH, random.choice(images))

# رسالة الترحيب
def welcome_message(call):
    user = call.from_user
    username = f"[@{user.username}](https://t.me/{user.username})" if user.username else f"[{user.first_name}](tg://user?id={user.id})"

    text = f"""💰 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗗𝗘𝗔𝗥

𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀 ☑️

🚧 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗮𝗱𝗱 𝗺𝗲 𝘁𝗼 𝘆𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽 𝗮𝗻𝗱 𝗜 𝘄𝗶𝗹𝗹 𝘄𝗼𝗿𝗸 𝘁𝗵𝗲𝗿𝗲, 𝗗𝗼𝗻'𝘁 𝗳𝗼𝗿𝘁𝗲𝗴𝘁 𝘁𝗼 𝗺𝗮𝗸𝗲 𝗺𝗲 𝗮 𝗺𝗼𝗱𝗲𝗿𝗮𝘁𝗼𝗿 ⚡"""
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("Meun 📜", callback_data="menu")
    markup.add(btn)

    img = get_random_image()
    if img:
        with open(img, "rb") as photo:
            bot.edit_message_media(
                media=telebot.types.InputMediaPhoto(photo, caption=text, parse_mode="Markdown"),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup
            )
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode="Markdown", reply_markup=markup)

# قائمة الأوامر
def commands_message(call):
    text = """Available commands ⚓

- `/gen` In order to generate cards and is used as follows
  `/gen BIN Amount` example
  `/gen 49857302 15`
---------------------------------------------------
- `/paypal` Generate a fake ID, send it and try it! 💻
---------------------------------------------------
- `/otp` Check cards check CC Check (otp & LookUP3ds)
  It is used as follows
  `/otp cc|mm|yy|cvv`
---------------------------------------------------
- `/bin` For information BIN It is used as follows
  `/bin BIN`
  example `/bin 498503` 
  `/paypal` generate fake identity 📽
---------------------------------------------------
`/account` Know your balance, account subscription status and all information ⚙️

- `file ♡` Submit a file and it will be checked automatically! 🌀"""

    markup = telebot.types.InlineKeyboardMarkup()
    btn_back = telebot.types.InlineKeyboardButton("🔙", callback_data="back")
    markup.add(btn_back)

    img = get_random_image()
    if img:
        with open(img, "rb") as photo:
            bot.edit_message_media(
                media=telebot.types.InputMediaPhoto(photo, caption=text, parse_mode="Markdown"),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup
            )
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode="Markdown", reply_markup=markup)

# أوامر الرد التفاعلي
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user = message.from_user
    username = f"[@{user.username}](https://t.me/{user.username})" if user.username else f"[{user.first_name}](tg://user?id={user.id})"

    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("Meun 📜", callback_data="menu")
    markup.add(btn)

    text = f"""💰 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗗𝗘𝗔𝗥

𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀 ☑️

🚧 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗮𝗱𝗱 𝗺𝗲 𝘁𝗼 𝘆𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽 𝗮𝗻𝗱 𝗜 𝘄𝗶𝗹𝗹 𝘄𝗼𝗿𝗸 𝘁𝗵𝗲𝗿𝗲, 𝗗𝗼𝗻'𝘁 𝗳𝗼𝗿𝘁𝗲𝗴𝘁 𝘁𝗼 𝗺𝗮𝗸𝗲 𝗺𝗲 𝗮 𝗺𝗼𝗱𝗲𝗿𝗮𝘁𝗼𝗿 ⚡"""
    img = get_random_image()
    if img:
        with open(img, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "menu":
        commands_message(call)
    elif call.data == "back":
        welcome_message(call)
@bot.message_handler(commands=['gen'])
def generate_cards(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Oops! That Doesn't Look Like a Valid BIN. Example: `/gen BIN Amount` or `/gen BIN|MM|YY|CVV`", 
    parse_mode="Markdown") 

            return

        bin_input = parts[1]
        amount = int(parts[2]) if len(parts) > 2 else 10

        if "|" in bin_input:
            bin_parts = bin_input.split("|")
            bin_number = bin_parts[0]
            exp_month_fixed = bin_parts[1] if len(bin_parts) > 1 and bin_parts[1] else None
            exp_year_fixed = bin_parts[2] if len(bin_parts) > 2 and bin_parts[2] else None
            cvv_fixed = bin_parts[3] if len(bin_parts) > 3 and bin_parts[3] else None
        else:
            bin_number = bin_input
            exp_month_fixed = None
            exp_year_fixed = None
            cvv_fixed = None

        if not (6 <= len(bin_number) <= 13):
            bot.send_message(message.chat.id, "❌ Please enter a valid BIN with 6 to 13  digits.")
            return

        msg = bot.send_message(message.chat.id, "🔄 Generating cards…")
        time.sleep(2)
        bot.delete_message(message.chat.id, msg.message_id)

        with open(TOP_BIN_FILE, 'r') as f:
            bin_data = json.load(f)

        with open(FLAGS_FILE, 'r') as f:
            flags_data = json.load(f)

        bin_info = bin_data.get(bin_number[:6])
        if not bin_info:
            bot.send_message(message.chat.id, "📛 𝗕𝗜𝗡 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗼𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱 𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗿𝗿𝗲𝗰𝘁 𝗶𝘁 📛")
            return

        flag = flags_data.get(bin_info.get("flag", "UN"), "🏳️")
        cards = []

        def luhn_generate(bin_number):
            """ توليد بطاقة صالحة باستخدام خوارزمية Luhn """
            card = bin_number + "".join(str(random.randint(0, 9)) for _ in range(16 - len(bin_number) - 1))
            checksum = sum(int(digit) for digit in card) % 10
            last_digit = (10 - checksum) % 10
            return card + str(last_digit)

        def validate_luhn(card_number):
            """ التحقق من صلاحية البطاقة باستخدام خوارزمية Luhn """
            checksum = 0
            reverse_digits = card_number[::-1]
            for i, digit in enumerate(reverse_digits):
                n = int(digit)
                if i % 2 == 1:
                    n *= 2
                    if n > 9:
                        n -= 9
                checksum += n
            return checksum % 10 == 0

        def generate_valid_cards():
            """ توليد بطاقات صالحة 100% مع ضمان العدد المطلوب """
            valid_cards = []
            while len(valid_cards) < amount:
                card = luhn_generate(bin_number)
                if validate_luhn(card):
                    gen_month = exp_month_fixed or str(random.randint(1, 12)).zfill(2)
                    gen_year = exp_year_fixed or str(random.randint(2025, 2033))
                    gen_cvv = cvv_fixed or str(random.randint(100, 999))

                    valid_cards.append(f"{card}|{gen_month}|{gen_year}|{gen_cvv}")
            return valid_cards

        # توليد البطاقات الصالحة
        cards = generate_valid_cards()

        # إرسال النتائج
        if amount > 20:
            file_path = "/data/data/com.termux/files/home/generated_cards.txt"
            with open(file_path, "w") as file:
                file.write("\n".join(cards))
            bot.send_document(message.chat.id, open(file_path, "rb"), caption="📂 Here is your generated cards file.")
        else:
            result = f"Bin → `{bin_number}`\nAmount → `{amount}`\n\n" + "\n".join([f"`{c}`" for c in cards])
            result += f"\n\n𝐁𝐈𝐍 𝐈𝐧𝐟𝐨 ➜  `{bin_info['brand']} - {bin_info['type']} - {bin_info['scheme']}`\n𝐁𝐚𝐧𝐤 ➜ `{bin_info['bank']}`\n𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ➜  `{bin_info['country']}` {flag}"
            bot.send_message(message.chat.id, result)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error generating cards! {str(e)}")

with open("top_bin.json", "r", encoding="utf-8") as f:
    bin_data = json.load(f)

with open("flags.json", "r", encoding="utf-8") as f:
    country_flags = json.load(f)

@bot.message_handler(commands=["bin"])
def lookup_bin(message):
    user_id = message.from_user.id
    current_time = time.time()

    # الحماية من السبام
    if user_id in USER_LAST_BIN_REQUEST:
        time_since_last_request = current_time - USER_LAST_BIN_REQUEST[user_id]
        if time_since_last_request < 5:
            remaining_time = int(5 - time_since_last_request)
            bot.reply_to(message, f"⛔ 𝗔𝗡𝗧𝗜 𝗦𝗽𝗮𝗺 𝗗𝗲𝘁𝗲𝗰𝘁𝗲𝗱!\n\n🔄 𝗧𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗮𝗳𝘁𝗲𝗿 {remaining_time} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀.")
            return

    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "📛 Please enter correct like `/bin 498503` ♜", parse_mode="Markdown")
            return

        bin_number = args[1]
        if not bin_number.isdigit() or len(bin_number) != 6:
            bot.reply_to(message, "Please Enter BIN from 6 numbers ❌", parse_mode="Markdown")
            return

        # تسجيل وقت البحث
        USER_LAST_BIN_REQUEST[user_id] = current_time

        # إرسال رسالة "جاري البحث..."
        loading_message = bot.reply_to(message, "Searching Wait 🔎…")

        # البحث عن معلومات الـ BIN
        info = bin_data.get(bin_number)
        if not info:
            bot.edit_message_text("This BIN is not found ,Sorry, choose a valid one 🚫", chat_id=message.chat.id, message_id=loading_message.message_id)
            return

        # استخراج البيانات المطلوبة
        bank_name = info.get("bank", "Unknown Bank")
        country_code = info.get("flag", "Unknown")  # الرمز المختصر للدولة
        country_name = info.get("country", "Unknown Country")
        country_flag = country_flags.get(country_code, "🚩")

        result = f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

𝗕𝗜𝗡 ⇾ <code>{bin_number}</code>
------------------------------
𝗜𝗻𝗳𝗼 ⇾ <code>{info.get("scheme", "Unknown").upper()} - {info.get("type", "Unknown").upper()} - {info.get("brand", "Unknown")}</code>
------------------------------
𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ <code>{bank_name}</code>
------------------------------
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ <code>{country_name} {country_flag}</code>

𝗕𝐲 🛡: <a href="https://t.me/iyad_ar">ᵝᵒˢˢ᭄•𒆜فخمツ</a>
"""
        bot.edit_message_text(result, chat_id=message.chat.id, message_id=loading_message.message_id, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

@bot.message_handler(commands=['paypal'])
def generate_single_fake_identity(message):
    try:
        # تعريف Faker داخل الأمر
        fake = Faker()

        # إرسال رسالة مؤقتة
        msg = bot.send_message(message.chat.id, "🔄 Generating identity, please wait...")

        # انتظار 3 ثواني
        time.sleep(0)

        # تعديل الرسالة وإرسال الصورة من مجلد التحميلات في أندرويد
        image_path = "/storage/emulated/0/Download/Paypal/-5794327524652730412_120.jpg"
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

        # توليد بيانات هوية واحدة فقط
        name1 = fake.name()
        name2 = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address().replace("\n", ", ")  # تنسيق العنوان
        passport = fake.random_int(min=100000000, max=999999999)

        # توليد رقم بطاقة عشوائي بصيغة BIN
        bin_number = f"/gen {random.randint(400000, 499999)}{random.randint(100000, 999999)}|12|26"

        identity_info = (
            f"🧒🏻 Full Name 1: `{name1}`\n"
            f"👤 Full Name 2: `{name2}`\n"
            f"📧 Email: `{email}`\n"
            f"📞 Phone Number: `{phone}`\n"
            f"🏠 Address: `{address}`\n"
            f"🛂 Passport Number: `{passport}`\n"
            f"💳 Bin: `{bin_number}`\n"
            "----------------------"
        )

        # إرسال هوية واحدة فقط
        bot.send_message(message.chat.id, identity_info, parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
def load_vip_data():
    try:
        with open("vip_data.json", "r") as file:
            return json.load(file)  # تحميل البيانات كـ dictionary
    except FileNotFoundError:
        return {}

# حساب الوقت المتبقي (عرض الساعات والدقائق فقط)
def time_left(expiration_time: str) -> str:
    expiration = datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S")
    current_time = datetime.now()
    if expiration < current_time:
        return None  # الاشتراك انتهى
    remaining_time = expiration - current_time
    
    # استخراج الساعات والدقائق فقط
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"  # تنسيق HH:MM

# التعامل مع الأمر /account
@bot.message_handler(commands=['account'])
def account(message):
    user_id = str(message.from_user.id)
    vip_data = load_vip_data()

    # طباعة محتوى vip_data لفحصه
    print(vip_data)

    if user_id in vip_data:
        expiration_time = vip_data[user_id]
        remaining_time = time_left(expiration_time)
        
        if remaining_time:
            bot.reply_to(message, f"The time remaining until your subscription expires is: {remaining_time}")
        else:
            bot.reply_to(message, "Your subscription has expired, please subscribe again 🔌")
    else:
        bot.reply_to(message, "You are not subscribed, sorry 📛")
# دالة فحص OTP
def get_bin_info(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# دالة لتحويل كود الدولة إلى علم باستخدام Unicode
def get_country_flag(country_code):
    if not country_code:
        return "❌"
    return "".join(chr(127397 + ord(c)) for c in country_code.upper())

@bot.message_handler(commands=['otp'])
def otp(message):
    try:
        args = message.text.split(' ')
        if len(args) != 2:
            bot.send_message(message.chat.id, "Please provide card information in the format: <code>cc|mm|yy|cvv</code>", parse_mode='HTML')
            return

        card_info = args[1]
        card_details = card_info.split('|')

        if len(card_details) != 4:
            bot.send_message(message.chat.id, "Invalid format! Use: <code>cc|mm|yy|cvv</code>", parse_mode='HTML')
            return

        card_number, month, year, cvv = card_details
        bin_number = card_number[:6]

        # إرسال رسالة انتظار أولية
        waiting_message = bot.send_message(message.chat.id, "Checking OTP 🤔...", parse_mode='HTML')

        # قراءة ملف Bin.txt لمعرفة إن كان الـ BIN موجودًا
        try:
            with open("Bin.txt", "r") as file:
                bin_data = file.read().splitlines()
        except FileNotFoundError:
            bin_data = []

        # التحقق مما إذا كان BIN موجودًا في الملف
        if bin_number in bin_data:
            result = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response = "Successful payment (LookUP3DS)"
            gate = "Braintree 🔰"
        else:
            result = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
            response = "Payment unsuccessful "
            gate = "Braintree 🔰"

        # جلب معلومات BIN من API
        bin_info = get_bin_info(bin_number)

        # تجهيز البيانات المسترجعة
        country_code = bin_info.get("country", {}).get("alpha2", "") if bin_info else ""
        country_flag = get_country_flag(country_code)
        country_name = bin_info.get("country", {}).get("name", "----") if bin_info else "----"

        result_message = f"""<b>Result:</b> {result}

<b>Card:</b> <code>{card_number}|{month}|{year}|{cvv}</code>

<b>Response:</b> {response}

<b>Gateway:</b> 3DS Lookup
<b>Gate:</b> {gate}
---
"""

        if bin_info:
            result_message += f"""<b>BIN:</b> {bin_number}
<b>Info:</b> {bin_info.get('type', '----')}
<b>Issuer:</b> {bin_info.get('bank', {}).get('name', '----')}
<b>Country:</b> {country_name} {country_flag}
<b>Other:</b> {bin_info.get('scheme', '----').upper()}
---
"""
        else:
            result_message += "<b>BIN Information:</b> Data not available ❌\n"

        result_message += "◆ 🌃◆"

        # الانتظار 3 ثوانٍ قبل تحديث الرسالة
        time.sleep(3)

        # تحديث الرسالة السابقة بدل إرسال رسالة جديدة
        bot.edit_message_text(result_message, chat_id=message.chat.id, message_id=waiting_message.message_id, parse_mode='HTML')

    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Error:</b> <code>{str(e)}</code>", parse_mode='HTML')
import logging  
logging.basicConfig(level=logging.INFO)  
  
def load_vip_data():  
    try:  
        with open(VIP_FILE, 'r') as f:  
            return json.load(f)  
    except FileNotFoundError:  
        return {}  
  
def update_vip_data(data):  
    with open(VIP_FILE, 'w') as f:  
        json.dump(data, f, indent=4)  
  
def is_user_vip(user_id):  
    vip_data = load_vip_data()  
    if str(user_id) in vip_data:  
        expiry_time = datetime.strptime(vip_data[str(user_id)], '%Y-%m-%d %H:%M:%S')  
        if expiry_time > datetime.now():  
            return True  
    return False  
  
def load_bins():  
    with open('Bin.txt', 'r') as f:  
        bins = [line.strip() for line in f.readlines()]  
    return bins  
  
def luhn_check(card_number):  
    total = 0  
    reverse_digits = card_number[::-1]  
    for i, digit in enumerate(reverse_digits):  
        n = int(digit)  
        if i % 2 == 1:  
            n *= 2  
            if n > 9:  
                n -= 9  
        total += n  
    return total % 10 == 0  
  
def read_cards(file_url):  
    response = requests.get(file_url)  
    if response.status_code == 200:  
        return response.text.splitlines()  
    return []  
  
def validate_card(card, bins):  
    parts = card.split('|')  
    if len(parts) != 4:  
        return False  
    cc, mm, yy, cvv = parts  
    bin6 = cc[:6].strip()  
    return bin6 in bins and luhn_check(cc.strip())  
  
stop_checking = {}  
@bot.message_handler(content_types=['document'])  
def handle_document(message):  
    chat_id = message.chat.id  
    file_id = message.document.file_id  # استخدام file_id من الرسالة  
  
    # التحقق من الاشتراك قبل إرسال الفاتورة  
    if not is_user_vip(message.from_user.id):  
        plan_time = 1  # الاشتراك لمدة يوم واحد  
        price = 5  # تكلفة الاشتراك (بالوحدات المناسبة)  
        expire = datetime.now() + timedelta(days=plan_time)  
        prices = [LabeledPrice(label='VIP', amount=int(price * 1))]  # سعر الاشتراك بالعملة (XTR)  
  
        try:  
            # إرسال الفاتورة مباشرة  
            bot.send_invoice(  
                chat_id=chat_id,  
                title='اشتراك يوم 1 📨',  
                description="""خطة VIP المميزة ⚡  
━━━━━━━━━━━━━━━━━  
قم بالحصول وفتح كل الأدوات والبوابات وكذلك الفحص عبر الملفات وتخطي الحظر عبر هاته الخطة 😍  
انت حالتك غير مشترك 📛  
━━━━━━━━━━━━━━━━━  
قم بدفع 5 نجمة وستحصل على اشتراك لمدة يوم واحد ⚡✅  
الثمن  
5 ⭐   
♡ اكمل الدفع 🥊  
━━━━━━━━━━━━━━━━━""",  
                invoice_payload=f'{chat_id}_{expire}',  
                provider_token='YOUR_PROVIDER_TOKEN',  # يجب إدخال الـ token الخاص بمزود الدفع  
                currency='XTR',  
                prices=prices  
            )  
        except Exception as e:  
            # في حال حدوث خطأ عند إرسال الفاتورة  
            bot.send_message(chat_id, f"❌ حدث خطأ أثناء إرسال الفاتورة: {str(e)}")  
            return  
    else:  
        # إذا كان المستخدم مشتركًا بالفعل، يتم بدء الفحص  
        start_card_check(chat_id, file_id)  
  
def start_card_check(chat_id, file_id):  
    stop_checking[chat_id] = False  
  
    # التحقق من وجود الملف باستخدام file_id  
    try:  
        file_info = bot.get_file(file_id)  # استخدام file_id الصحيح هنا  
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"  
    except Exception as e:  
        bot.send_message(chat_id, f"❌ حدث خطأ في الحصول على الملف: {str(e)}")  
        return  
  
    # قراءة البطاقات  
    cards = read_cards(file_url)  
    if not cards:  
        bot.send_message(chat_id, "❌ فشل في قراءة الملف أو أنه فارغ.")  
        return  
  
    total_count = len(cards)  
  
    # إرسال رسالة "قراءة الملف..."  
    sent_msg = bot.send_message(chat_id, "𝙿𝚕𝚎𝚊𝚜𝚎 𝚆𝚊𝚒𝚝 𝙲𝚑𝚎𝚌𝚔𝚒𝚗𝚐 𝚢𝚘𝚞𝚛 𝙲𝚊𝚛𝚍...⌛")  
  
    time.sleep(0.1)  
    bot.delete_message(chat_id, sent_msg.message_id)  
  
    # إرسال رسالة الفحص  
    processing_msg = bot.send_message(chat_id, "🔍 Checking …")  
  
    bins = load_bins()  
  
    approved_count = 0  
    dead_count = 0  
  
    # بدأ الفحص  
    for card in cards:  
        if stop_checking[chat_id]:  # إذا تم الضغط على زر STOP 🚧  
            break  
  
        time.sleep(random.randint(2, 3))  # تأخير بين كل فحص  
        if validate_card(card, bins):  
            approved_count += 1  
        else:  
            dead_count += 1  
  
        # تحديث الأزرار الشفافة مع البطاقة الحالية  
        markup = InlineKeyboardMarkup(row_width=1)  
        markup.add(  
            InlineKeyboardButton(f" {card}", callback_data='current_card'),  
            InlineKeyboardButton(f"☑️ 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝: {approved_count}", callback_data='approved'),  
            InlineKeyboardButton(f"⛔ Dead: {dead_count}", callback_data='dead'),  
            InlineKeyboardButton(f"⭐ Total: {total_count}", callback_data='total'),  
            InlineKeyboardButton("🚧 STOP", callback_data='stop')  
        )  
  
        # تحديث الرسالة كل ثانية  
        bot.edit_message_text("The examination has started 🔋 please wait … You are subscribed to VIP 🧾 Checking now, wait … ", chat_id, processing_msg.message_id, reply_markup=markup)  
        time.sleep(0.01)  
  
    # إذا تم الضغط على STOP  
    if stop_checking[chat_id]:  
        final_msg = "🛑\n\n"  
    else:  
        final_msg = "✅\n\n"  
  
    final_msg += f"☑️ Approved: {approved_count}\n⛔ Dead: {dead_count}\n⭐ Total: {total_count}"  
  
    # إرسال النتيجة النهائية  
    markup = InlineKeyboardMarkup(row_width=1)  
    markup.add(  
        InlineKeyboardButton(f"☑️ 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝: {approved_count}", callback_data='approved'),  
        InlineKeyboardButton(f"⛔ Dead: {dead_count}", callback_data='dead'),  
        InlineKeyboardButton(f"⭐ Total: {total_count}", callback_data='total')  
    )  
    bot.edit_message_text(final_msg, chat_id, processing_msg.message_id, reply_markup=markup)  
  
@bot.pre_checkout_query_handler(func=lambda query: True)  
def checkout_handler(pre_checkout_query: PreCheckoutQuery):  
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  
  
@bot.message_handler(content_types=['successful_payment'])  
def successful_payment_handler(message):  
    chat_id = message.chat.id  
    user_id = message.from_user.id  
  
    # تخزين تاريخ انتهاء الاشتراك للمستخدم  
    vip_data = load_vip_data()  
    expire_time = datetime.now() + timedelta(days=1)  
    vip_data[str(user_id)] = expire_time.strftime('%Y-%m-%d %H:%M:%S')  
  
    update_vip_data(vip_data)  
  
    # بدء الفحص بعد الدفع الناجح  
    start_card_check(chat_id)  
  
    bot.send_message(chat_id, "تم الدفع بنجاح! شكرًا لشرائك. أنت الآن مشترك في خطة VIP لمدة يوم واحد. ⚡")  
  
@bot.callback_query_handler(func=lambda call: call.data == 'stop')  
def stop_processing(call):  
    global stop_checking  
    chat_id = call.message.chat.id  
    stop_checking[chat_id] = True  
    bot.answer_callback_query(call.id, "🛑")  
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# حفظ البيانات إلى الملف
def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# إنشاء كود عشوائي
def generate_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))

# تحميل البيانات
vip_data = load_json(VIP_FILE)
codes_data = load_json(CODES_FILE)

# أمر /c لإنشاء كود
@bot.message_handler(commands=['c'])
def create_code(message):
    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "❌ 𝒀𝒐𝒖 𝒅𝒐 𝒏𝒐𝒕 𝒉𝒂𝒗𝒆 𝒑𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏.")
        return

    msg = bot.reply_to(message, "📌 𝑬𝒏𝒕𝒆𝒓 𝒕𝒉𝒆 𝒏𝒖𝒎𝒃𝒆𝒓 𝒐𝒇 𝒖𝒔𝒆𝒓𝒔 𝒂𝒍𝒍𝒐𝒘𝒆𝒅 𝒑𝒆𝒓 𝒄𝒐𝒅𝒆:")
    bot.register_next_step_handler(msg, process_user_count)

def process_user_count(message):
    try:
        max_users = int(message.text)
        msg = bot.reply_to(message, "⏳ 𝑬𝒏𝒕𝒆𝒓 𝒔𝒖𝒃𝒔𝒄𝒓𝒊𝒑𝒕𝒊𝒐𝒏 𝒕𝒊𝒎𝒆 (𝐇𝐇:𝐌𝐌):")
        bot.register_next_step_handler(msg, lambda m: process_subscription_time(m, max_users))
    except ValueError:
        bot.reply_to(message, "❌ 𝑰𝒏𝒗𝒂𝒍𝒊𝒅 𝒏𝒖𝒎𝒃𝒆𝒓.")

def process_subscription_time(message, max_users):
    try:
        time_parts = message.text.split(":")
        if len(time_parts) != 2:
            raise ValueError
        
        hours, minutes = map(int, time_parts)
        duration = f"{hours:02}:{minutes:02}"  # حفظ فقط HH:MM

        code = generate_code()
        codes_data[code] = {"max_users": max_users, "used_users": [], "duration": duration}

        save_json(CODES_FILE, codes_data)

        bot.reply_to(message, f"✅ 𝑪𝒐𝒅𝒆 𝒄𝒓𝒆𝒂𝒕𝒆𝒅 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚:\n`{code}`", parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "❌ 𝑬𝒏𝒕𝒆𝒓 𝒕𝒊𝒎𝒆 𝒊𝒏 𝒇𝒐𝒓𝒎𝒂𝒕 𝐇𝐇:𝐌𝐌.")

# أمر /reedem لتفعيل الكود
@bot.message_handler(commands=['reedem'])
def redeem_code(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    
    if len(args) != 2:
        bot.reply_to(message, "❌ 𝑪𝒐𝒓𝒓𝒆𝒄𝒕 𝒖𝒔𝒂𝒈𝒆:\n`/reedem <code>`", parse_mode="Markdown")
        return
    
    code = args[1]
    
    if code not in codes_data:
        bot.reply_to(message, "📛 𝑰𝒏𝒗𝒂𝒍𝒊𝒅 𝒄𝒐𝒅𝒆.")
        return
    
    code_info = codes_data[code]

    if user_id in code_info["used_users"]:
        bot.reply_to(message, "📛 𝑰 𝒖𝒔𝒆𝒅 𝒕𝒉𝒆 𝒎𝒂𝒙𝒊𝒎𝒖𝒎 𝒐𝒏 𝒆𝒂𝒄𝒉 𝒂𝒄𝒄𝒐𝒖𝒏𝒕, 𝒕𝒓𝒚 𝒐𝒏 𝒂𝒏𝒐𝒕𝒉𝒆𝒓 𝒂𝒄𝒄𝒐𝒖𝒏𝒕.")
        return
    
    if len(code_info["used_users"]) >= code_info["max_users"]:
        bot.reply_to(message, "📛 𝑻𝒉𝒆 𝒄𝒐𝒅𝒆 𝒉𝒂𝒔 𝒆𝒙𝒑𝒊𝒓𝒆𝒅.")
        return
    
    # الحصول على مدة الاشتراك الأصلية
    duration = code_info["duration"]

    # حساب وقت الانتهاء
    try:
        hours, minutes = map(int, duration.split(":"))
        expiry_time = datetime.now() + timedelta(hours=hours, minutes=minutes)
    except ValueError:
        bot.reply_to(message, "❌ 𝑬𝒓𝒓𝒐𝒓 𝒑𝒓𝒐𝒄𝒆𝒔𝒔𝒊𝒏𝒈 𝒕𝒉𝒆 𝒄𝒐𝒅𝒆.")
        return

    # إضافة المستخدم إلى قائمة المستخدمين المستفيدين
    code_info["used_users"].append(user_id)
    vip_data[user_id] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")

    save_json(CODES_FILE, codes_data)
    save_json(VIP_FILE, vip_data)

    bot.reply_to(message, f"🎁 𝑻𝒉𝒆 𝒄𝒐𝒅𝒆 𝒉𝒂𝒔 𝒃𝒆𝒆𝒏 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚 𝒓𝒆𝒅𝒆𝒆𝒎𝒆𝒅!\n\n"
                          f"☞ 𝑵𝒖𝒎𝒃𝒆𝒓 𝒐𝒇 𝒑𝒆𝒐𝒑𝒍𝒆 𝒓𝒆𝒎𝒂𝒊𝒏𝒊𝒏𝒈: {code_info['max_users'] - len(code_info['used_users'])}\n"
                          f"⌚ 𝑨𝒅𝒅𝒆𝒅 𝒕𝒊𝒎𝒆: {duration}")

print("Done1")
print("Done2")
bot.polling(non_stop=True, interval=0)
