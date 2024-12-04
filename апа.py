import telebot
from rule34Py import rule34Py


class MyBot:
    def __init__(self, token):
        # Инициализация бота с токеном и объекта rule34Py
        self.bot = telebot.TeleBot(token)
        self.r34Py = rule34Py()
        self.register_handlers()

    def register_handlers(self):
        # Регистрация обработчиков команд
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['sigma'])(self.get_astolfo)
        self.bot.message_handler(content_types=['text'])(self.process_message)

    def start(self, message):
        # Обработчик команды /start, отправляет сообщение о помощи
        self.bot.send_message(message.chat.id, 'Динаху ссылка на использование: \n https://telegra.ph/femboj-bot-08-27')

    def get_astolfo(self, message):
        # Обработчик команды /sigma, отправляет случайную картинку с тегом "astolfo_(fate)"
        tag = ["astolfo_(fate) sort:score -video -animation"]
        self.send_post(message, tag)

    def process_message(self, message):
        # Основной обработчик текстовых сообщений
        text = message.text.lower()
        if text.startswith('r34 '):
            # Обработка команды с тегами r34
            self.handle_r34_command(message, text)
        elif text.startswith('se '):
            # Обработка команды с поиском по ID
            self.handle_se_command(message, text)

    def handle_r34_command(self, message, text):
        # Обработка команды r34 и получение постов по тегам
        try:
            tags = [tag.strip() for tag in text.split('r34 ')[1].strip().split(', ')]
            self.send_post(message, tags)
        except IndexError:
            # Если введён неверный формат команды
            self.bot.reply_to(message, "Неверный формат команды. Пример: r34 tag1, tag2")

    def handle_se_command(self, message, text):
        # Обработка команды se и получение тегов по ID
        try:
            idi = ''.join(filter(str.isdigit, text.split('se ')[1].strip()))
            if idi:
                self.se(message, idi)
            else:
                self.bot.reply_to(message, "Вы должны ввести числа после 'se '")
        except IndexError:
            # Если введён неверный формат команды
            self.bot.reply_to(message, "Неверный формат команды.")

    def send_post(self, message, tags):
        # Отправка поста по заданным тегам
        try:
            searcher = self.r34Py.random_post(tags)
            if searcher.image:
                # Если есть изображение, отправляем его
                self.bot.send_photo(message.chat.id, searcher.image, caption=f"ID: {searcher.id}")
            elif searcher.video:
                # Если есть видео, отправляем его
                self.bot.send_video(message.chat.id, searcher.video, caption=f"ID: {searcher.id}")
        except Exception as e:
            # Обработка ошибки при получении поста
            self.bot.reply_to(message, f"Произошла ошибка: {str(e)}")

    def se(self, message, idi):
        # Получение тегов по ID поста и отправка их в ответ
        try:
            post = self.r34Py.get_post(idi)
            tags = ", ".join(post.tags)
            self.bot.reply_to(message, f"Теги для ID {idi}: {tags}")
        except Exception as e:
            # Обработка ошибки при получении поста по ID
            self.bot.reply_to(message, f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    my_bot = MyBot("ваш токен")
    my_bot.bot.polling(none_stop=True)
