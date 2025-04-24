import sqlite3
from telebot import types

# === FAQ данные ===
faq_data = {
    "Какие профессии самые востребованные?": "Сейчас в топе IT-специальности, врачи, инженеры и логисты.",
    "Как выбрать профессию по интересам?": "Лучше пройти профориентационный тест или определить свои сильные стороны.",
    "Сколько зарабатывает дизайнер?": "В среднем от 80 до 150 тысяч рублей, в зависимости от специализации и опыта."
}

# === Клавиатура с FAQ ===
def get_faq_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*faq_data.keys(), "Другое")
    return markup

def get_faq_answer(question_text):
    return faq_data.get(question_text)

# === Инициализация БД ===
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

# === Сохранение вопроса пользователя ===
def save_question_to_db(user_id, username, question_text):
    conn = sqlite3.connect("profession.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (user_id, username, question) VALUES (?, ?, ?)", 
                   (user_id, username, question_text))
    conn.commit()
    conn.close()
