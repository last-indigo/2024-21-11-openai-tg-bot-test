import os
from dotenv import load_dotenv
import telebot
from openai import OpenAI

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Я бот на основе ChatGPT.")

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружественный ассистент"},
                {"role": "user", "content": message.text}
            ],
            max_tokens=300
        )
        
        bot_response = response.choices[0].message.content
        bot.reply_to(message, bot_response)
    
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

bot.delete_webhook()
bot.polling(none_stop=True)
