import telebot
from flask import Flask, request
import threading
import os
import time
from cardinal import Cardinal

# ===== НАСТРОЙКИ =====
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')
GOLDEN_KEY = os.environ.get('GOLDEN_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

# ===== ВЕБ-СЕРВЕР ДЛЯ WEBHOOK =====
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 400

@app.route('/health')
def health():
    return 'OK', 200

# ===== ТВОИ ОБЫЧНЫЕ ОБРАБОТЧИКИ =====
@bot.message_handler(commands=['start'])
def start(message):
    if str(message.chat.id) == ADMIN_ID:
        bot.reply_to(message, "✅ Бот запущен и работает через Webhook!")

# ... сюда добавь ВСЕ свои остальные обработчики (автовыдача, проверка и т.д.)

# ===== ЗАПУСК =====
if __name__ == '__main__':
    # Устанавливаем webhook
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/webhook"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print(f"Webhook установлен: {webhook_url}")
    
    # Запускаем веб-сервер
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
