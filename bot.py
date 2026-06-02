import telebot
from google import genai

# === ТВОИ ГОТОВЫЕ КЛЮЧИ ===
BOT_TOKEN = '8904201516:AAHgJQOotlCvsWSzSstH6uhiRGvuGEQlqbU'
AI_KEY = 'AQ.Ab8RN6KVEbBrC2cj3IM8pp3c09Zb1ske4I7P-SGCEXG-gAg3qw'
# ==========================

# Подключаем бота и ИИ
bot = telebot.TeleBot(BOT_TOKEN)
ai_client = genai.Client(api_key=AI_KEY)

# Ответ на команду /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Привет! Твой личный ИИ-бот успешно запущен и готов к работе. Напиши мне любой вопрос!")

# Пересылка сообщений в ИИ и возврат ответа обратно в Telegram
@bot.message_handler(func=lambda message: True)
def talk_to_ai(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка в коде ИИ. Проверь ключи.")
        print(f"Ошибка: {e}")

# Запуск бота
bot.infinity_polling()