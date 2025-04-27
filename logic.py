import sqlite3
from telebot import types
from openai import OpenAI
from config import *


client = OpenAI(api_key=OPENAI_API_KEY)


# Самые популярные вопросы 
faq_data = {
    "Какие профессии самые востребованные?": "Сейчас в топе IT-специальности, врачи, инженеры и логисты.",
    "Как выбрать профессию по интересам?": "Лучше пройти профориентационный тест или определить свои сильные стороны.",
    "Сколько зарабатывает дизайнер?": "В среднем от 80 до 150 тысяч рублей, в зависимости от специализации и опыта."
}

def get_faq_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*faq_data.keys(), "Другое")
    return markup

def get_faq_answer(question_text):
    return faq_data.get(question_text)

def init_db():
    conn = sqlite3.connect("profession.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            question TEXT
        )
    """)
    conn.commit()
    conn.close()

# Сохранение вопроса пользователя 
def save_question_to_db(user_id, username, question_text):
    conn = sqlite3.connect("profession.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (user_id, username, question) VALUES (?, ?, ?)", 
                   (user_id, username, question_text))
    conn.commit()
    conn.close()


def get_professions_by_criteria(interests, education, income, work_type):
    conn = sqlite3.connect("profession.db")
    cursor = conn.cursor()

    query = """
        SELECT name FROM professions_criteries
        WHERE interests LIKE ?
        AND education LIKE ?
        AND income LIKE ?
        AND work_type LIKE ?
    """

    cursor.execute(query, (
        f"%{interests}%",
        f"%{education}%",
        f"%{income}%",
        f"%{work_type}%"
    ))

    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def get_profession_from_gpt(interest, education, income, work_type):
    prompt = f"Пользователь ищет профессию с интересами '{interest}', уровнем образования '{education}', ожидаемым доходом '{income}', типом работы '{work_type}'. Предложи подходящую профессию в виде ответа как: Профессия которая вам подходит это: 'профессия'"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты помощник по выбору профессий."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    profession = response.choices[0].message.content.strip()
    return profession