from config import TOKEN
import telebot
from logic import *
from telebot import types

bot = telebot.TeleBot(TOKEN)
init_db()

# Храним ID пользователей, которых уже поприветствовали
welcomed_users = set()

@bot.message_handler(commands=['hello'])
def send_welcome(message):
    user_id = message.from_user.id

    if user_id not in welcomed_users:
        welcomed_users.add(user_id)
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! 👋 Добро пожаловать в нашего бота! \nНапиши команду /help что бы узнать какие команды я могу исполнять, \nа так же /ask_question если у тебя есть вопросы ко мне!"
        )
    else:
        bot.send_message(message.chat.id, "С возвращением! Напиши /help для команд или /ask_question для вопросов.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Я выполняю 4 команды:\n"
                          "1. /ask_question — Часто задаваемые вопросы или задай свой.\n"
                          "2. /select — Я предложу тебе подходящие профессии.\n"
                          "3. /input — Введи свои критерии, и я предложу профессию.\n"
                          "4. /info — Расскажу о профессии по названию.")
    

@bot.message_handler(commands=['ask_question']) #бот сначала показывает самые задаваемые, и на выбор пользователя, отвечает на вопрос. Если пользователь выберет 'другое' тогда вопрос пользователя отправляется в базу данных вопросов, и потом реальный человек, отвечает ему лично
def ask_question(message):
    markup = get_faq_keyboard()
    bot.send_message(
        message.chat.id,
        "Вот список популярных вопросов. Выберите один или нажмите 'Другое', чтобы задать свой:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in [
    "Какие профессии самые востребованные?",
    "Как выбрать профессию по интересам?",
    "Сколько зарабатывает дизайнер?"
])
def handle_faq_answer(message):
    answer = get_faq_answer(message.text)
    if answer:
        bot.send_message(message.chat.id, answer, reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text == "Другое")
def handle_custom_question_request(message):
    bot.send_message(message.chat.id, "Пожалуйста, напиши свой вопрос. Наш специалист ответит тебе лично.", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, save_custom_question)

def save_custom_question(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Без ника"
    question_text = message.text

    save_question_to_db(user_id, username, question_text)

    bot.send_message(message.chat.id, "Спасибо! Мы получили ваш вопрос и скоро ответим лично.")


@bot.message_handler(commands=['select']) #бот сам предлагает критерии и подбирает профессию
def select_criteries():
    pass

@bot.message_handler(commands=['input']) #пользователь сам вводит свои критерии, бот через chat gpt предлагает профессию
def input_criteries():
    pass

@bot.message_handler(commands=['info']) #бот подробно рассказывает о профессии по названию
def info_profession():
    pass

# Запуск
print("Бот работает...")
if __name__ == "__main__":
    bot.polling(none_stop=True)