import os
from dotenv import load_dotenv
import telebot
import openai
from flask import Flask, request

# Загрузка переменных окружения
load_dotenv()

# Initialize bot and OpenAI
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
openai.api_key = os.getenv('OPENAI_API_KEY')

# Flask для webhook
app = Flask(__name__)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
   welcome_text = """
👋 Привет! Я бот на основе ChatGPT.
🤖 Могу помочь с:
- Ответами на вопросы
- Написанием текстов
- Решением задач
- Генерацией идей
Просто напиши мне сообщение!
"""
   bot.reply_to(message, welcome_text)

# Основной обработчик сообщений
@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
   try:
       # Отправка запроса в OpenAI
       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=[
               {"role": "system", "content": "Ты дружественный ассистент"},
               {"role": "user", "content": message.text}
           ],
           max_tokens=300  # Ограничение длины ответа
       )
       
       # Получение ответа
       bot_response = response.choices[0].message.content
       
       # Отправка ответа пользователю
       bot.reply_to(message, bot_response)
   
   except Exception as e:
       bot.reply_to(message, f"Произошла ошибка: {e}")

# Запуск бота
bot.polling(none_stop=True)
