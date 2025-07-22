import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

bot = telebot.TeleBot(BOT_TOKEN)

def web_app_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    web_app = types.WebAppInfo("https://your-domain.com")
    button = types.KeyboardButton(text="🍳 Открыть рецепты", web_app=web_app)
    keyboard.add(button)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот с рецептами. Нажми на кнопку ниже, чтобы открыть приложение:",
        reply_markup=web_app_keyboard()
    )

@bot.message_handler(content_types=['web_app_data'])
def web_app_handler(message):
    data = message.web_app_data.data
    bot.send_message(
        message.chat.id,
        f"Добавлено в корзину: {data}"
    )

if __name__ == '__main__':
    print("Bot started...")
    bot.infinity_polling()
