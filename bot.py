import os
from dotenv import load_dotenv
import telebot
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv()

# Initialize bot and OpenAI
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
        response = client.chat.completions.create(
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

bot.delete_webhook()
bot.polling(none_stop=True)
