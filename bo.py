import telebot
import requests
import random
from luhn import verify

# Bot Token
TOKEN = "7312710877:AAGM765_nOLlpzzaAlNP0ib6KKxojt2bC18"

# Create bot instance
bot = telebot.TeleBot(TOKEN)

def generate_valid_card(bin_prefix):
    """Generate valid cards based on a 6-digit BIN number."""
    base = bin_prefix
    cards = set()

    while len(cards) < 10:
        card = base + "".join(str(random.randint(0, 9)) for _ in range(16 - len(base)))
        if verify(card):
            month = str(random.randint(1, 12)).zfill(2)
            year = str(random.randint(23, 28))
            cvv = str(random.randint(100, 999))
            cards.add(f"{card}|{month}|{year}|{cvv}")

    return list(cards)

@bot.message_handler(commands=['start'])
def start_command(message):
    """Send a welcome message explaining the bot."""
    bot.reply_to(message, 
        "Welcome to the BIN Generator Bot! 🤖\n\n"
        "Use the following command to generate valid cards:\n"
        "👉 `/gen <6-digit BIN>`\n\n"
        "Example:\n"
        "`/gen 123456`\n\n"
        "Note: This bot generates random valid card numbers but does NOT verify if the BIN is real or belongs to a bank.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['gen'])
def gen_command(message):
    """Handle the /gen command to generate valid cards."""
    args = message.text.split()[1:]  # Get arguments after /gen
    if not args or len(args[0]) != 6 or not args[0].isdigit():
        bot.reply_to(message, "Please provide a valid 6-digit BIN: `/gen 123456`", parse_mode="Markdown")
        return

    bin_number = args[0]
    msg = bot.reply_to(message, "Generating...")

    cards = generate_valid_card(bin_number)
    if not cards:
        bot.edit_message_text("Failed to generate cards ❌", msg.chat.id, msg.message_id)
        return

    response = f"𝐁𝐈𝐍 ➜ {bin_number}\n\n" + "\n".join(cards)
    
    bot.edit_message_text(response, msg.chat.id, msg.message_id)

# Start the bot
bot.polling(none_stop=True)
