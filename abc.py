import telebot
token = '6838869729:AAGgt28OIcO6XOSKF-Njm3TPWoq52oG1xMo'


bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.infinity_polling()