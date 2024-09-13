import telebot
from rule34Py import rule34Py


bot = telebot.TeleBot("token")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'динаху ссылка на использование \n https://telegra.ph/femboj-bot-08-27')

r34Py = rule34Py()

@bot.message_handler(commands=['sigma'])
def get_astolfo(message):
    tag = ["astolfo_(fate) sort:score -video -animation"]
    try:
        searcher = r34Py.random_post(tag)
        bot.send_photo(message.chat.id, searcher.image)
    except:
        bot.reply_to(message, "те кто сделал этот пост пидарасища")

@bot.message_handler(content_types=['text'])
def process_message(message):
    text = message.text.lower()
    if text.startswith('r34 '):
        try:
            tags = [tag.strip() for tag in text.split('r34 ')[1].strip().split(', ')]
            get_r34(message, tags)
        except:
            bot.reply_to(message, "разраб еблан")
    elif text.startswith('se '):
        try:
            idi = ''.join(filter(str.isdigit, text.split('se ')[1].strip()))
            if idi:
                se(message, idi)
            else:
                bot.reply_to(message, "Вы должны ввести числа после 'se '")
        except:
            bot.reply_to(message, "Разраб сами знаете кто")

def get_r34(message, tags):
    try:
        searcher = r34Py.random_post(tags)
        tags_1 = str(searcher.id)
        if searcher.image:
            bot.send_photo(message.chat.id, searcher.image, caption=f"ID: {tags_1}")
        elif searcher.video:
            bot.send_video(message.chat.id, searcher.video, caption=f"ID: {tags_1}")
        tags.clear()
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

def se(message, idi):
    try:
        post = r34Py.get_post(idi)
        tags = ", ".join(post.tags)
        bot.reply_to(message, f"Теги для ID {idi}: {tags}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

bot.polling()