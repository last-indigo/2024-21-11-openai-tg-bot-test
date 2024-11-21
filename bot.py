import os
import telebot
import openai
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и OpenAI
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
openai.api_key = os.getenv('OPENAI_API_KEY')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Привет! Я ChatGPT бот. Задай вопрос!")

@bot.message_handler(func=lambda message: True)
def chat_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный ассистент"},
                {"role": "user", "content": message.text}
            ],
            max_tokens=300
        )
        bot_response = response.choices[0].message.content
        bot.reply_to(message, bot_response)
    
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Webhook для Render
if __name__ == "__main__":
    bot.polling(none_stop=True)

