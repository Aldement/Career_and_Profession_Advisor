from config import TOKEN
import telebot
from logic import *
from telebot import types

bot = telebot.TeleBot(TOKEN)
init_db()

# Храним ID пользователей, которых уже поприветствовали
welcomed_users = set()
user_selections = {}

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
def select_criteries(message):
    user_id = message.from_user.id
    user_selections[user_id] = {}  # Сброс выбора пользователя
    ask_interest(message)

def ask_interest(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Работа с людьми", "Работа с техникой", "Творческая деятельность", "Научная работа")
    bot.send_message(message.chat.id, "Что вам ближе всего по интересам?", reply_markup=markup)
    bot.register_next_step_handler(message, handle_interest)

def handle_interest(message):
    user_id = message.from_user.id
    user_selections[user_id]['interest'] = message.text
    ask_education(message)

def ask_education(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Высшее", "Среднее специальное", "Не требуется")
    bot.send_message(message.chat.id, "Какой у вас уровень образования?", reply_markup=markup)
    bot.register_next_step_handler(message, handle_education)

def handle_education(message):
    user_id = message.from_user.id
    user_selections[user_id]['education'] = message.text
    ask_income(message)

def ask_income(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Низкий", "Средний", "Высокий")
    bot.send_message(message.chat.id, "Какой уровень дохода вы ожидаете?", reply_markup=markup)
    bot.register_next_step_handler(message, handle_income)

def handle_income(message):
    user_id = message.from_user.id
    user_selections[user_id]['income'] = message.text
    ask_work_type(message)

def ask_work_type(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Удалённая", "Офис", "Физический труд")
    bot.send_message(message.chat.id, "Предпочитаемый тип работы?", reply_markup=markup)
    bot.register_next_step_handler(message, show_profession_suggestions)

def show_profession_suggestions(message):
    user_id = message.from_user.id
    user_selections[user_id]['work_type'] = message.text
    selection = user_selections[user_id]

    professions = get_professions_by_criteria(
        selection['interest'],
        selection['education'],
        selection['income'],
        selection['work_type']
    )

    if professions: 
        response = "Вот подходящие профессии:\n" + "\n".join([f"- {p}" for p in professions])
    else:
        response = "Не удалось найти профессии по заданным критериям."

    bot.send_message(message.chat.id, response, reply_markup=types.ReplyKeyboardRemove())
    del user_selections[user_id]  # Очистка после ответа

@bot.message_handler(commands=['input'])  # Пользователь вводит свои критерии, бот через ChatGPT предлагает профессию
def input_criteries(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Напиши свои интересы, образование, ожидаемый доход и тип работы через запятую.\nНапример: 'Работа с людьми, Высшее, Средний, Офис'.")
    bot.register_next_step_handler(message, handle_input_criteria)

def handle_input_criteria(message):
    user_id = message.from_user.id
    criteria = message.text.split(',')

    if len(criteria) != 4:
        bot.send_message(message.chat.id, "Пожалуйста, укажи все 4 критерия (интересы, образование, доход, тип работы) через запятую.")
        return

    interest, education, income, work_type = map(str.strip, criteria)

    # Используем GPT для получения подходящей профессии
    profession = get_profession_from_gpt(interest, education, income, work_type)
    
    if profession:
        bot.send_message(message.chat.id, f"Вот подходящая профессия по твоим критериям: {profession}.")
    else:
        bot.send_message(message.chat.id, "Не удалось найти подходящую профессию. Попробуй изменить критерии.")

        
@bot.message_handler(commands=['info']) #бот подробно рассказывает о профессии по названию
def info_profession():
    pass

# Запуск
print("Бот работает...")
if __name__ == "__main__":
    bot.polling(none_stop=True)