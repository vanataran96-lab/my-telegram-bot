import os
import telebot
import google.generativeai as genai
import threading
import http.server

# Включаем микро-сервер, чтобы Render не ругался на порты
threading.Thread(target=lambda: http.server.HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 10000))), http.server.BaseHTTPRequestHandler).serve_forever(), daemon=True).start()

BOT_TOKEN = '8904201516:AAF1k_aX1DZUHZ81vQVdGZ9KfmD'
AI_KEY = 'AQ.Ab8RN6J_k0nYK958LDG78mLpBUoskQgTVHxP4Zj9OfgDIXfaaA'

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=AI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я твой ИИ бот. Напиши мне любой вопрос, и я отвечу!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка в коде ИИ. Проверь ключи.")

bot.polling(none_stop=True)
