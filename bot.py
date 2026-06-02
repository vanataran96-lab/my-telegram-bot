import os
import telebot
from google import genai
import threading
import http.server

# Микро-сервер для обмана Render портов
threading.Thread(target=lambda: http.server.HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 10000))), http.server.BaseHTTPRequestHandler).serve_forever(), daemon=True).start()

BOT_TOKEN = '8904201516:AAF1k_aXiDZUHZ81vQVdGZ9KfroDesd477c'
AI_KEY = 'AQ.Ab8RN6J_k0nYK958LDG78mLpBUoskQgTVHxP4Zj9OfgDIXfaaA'

bot = telebot.TeleBot(BOT_TOKEN)
# Используем новый официальный клиент Google GenAI
ai_client = genai.Client(api_key=AI_KEY)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я твой ИИ бот. Напиши мне любой вопрос, и я отвечу!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        # Новый синтаксис генерации контента
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        # Если упадет — мы увидим настоящую причину прямо в чате
        bot.send_message(message.chat.id, f"Ошибка ИИ: {str(e)}")

bot.polling(none_stop=True)
