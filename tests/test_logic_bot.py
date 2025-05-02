# test_logic.py
import pytest
from logic import *

def test_get_faq_answer_known():
    assert get_faq_answer("Какие профессии самые востребованные?") == \
           "Сейчас в топе IT-специальности, врачи, инженеры и логисты."

def test_get_faq_answer_unknown():
    assert get_faq_answer("Как стать космонавтом?") is None

def test_get_faq_keyboard_contains_expected_buttons():
    markup = get_faq_keyboard()
    button_texts = [button['text'] for row in markup.keyboard for button in row]

    assert "Какие профессии самые востребованные?" in button_texts
    assert "Как выбрать профессию по интересам?" in button_texts
    assert "Сколько зарабатывает дизайнер?" in button_texts
    assert "Другое" in button_texts

# Фикстура для чистой тестовой базы
@pytest.fixture(scope="function")
def test_db(tmp_path):
    test_db_path = tmp_path / "test_profession.db"
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()

    # Копируем структуру таблиц как в оригинале
    cursor.execute('''
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            question TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE professions_criteries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            interests TEXT,
            education TEXT,
            income TEXT,
            work_type TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Professions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT,
            description TEXT,
            responsibilities TEXT,
            advantages TEXT,
            disadvantages TEXT,
            average_salary DECIMAL(10, 2),
            education_requirements TEXT,
            skills_required TEXT,
            career_prospects TEXT
        )
    ''')

    conn.commit()
    conn.close()

    yield str(test_db_path)


def test_save_question_to_db(test_db, monkeypatch):
    # Сохраняем оригинальный connect
    original_connect = sqlite3.connect
    # Переопределяем connect только для logic
    monkeypatch.setattr("logic.sqlite3.connect", lambda _: original_connect(test_db))

    init_db()

    save_question_to_db(12345, "test_user", "Как выбрать профессию?")

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, question FROM questions")
    row = cursor.fetchone()
    conn.close()

    assert row == (12345, "test_user", "Как выбрать профессию?")


def test_get_professions_by_criteria(test_db, monkeypatch):
    original_connect = sqlite3.connect
    monkeypatch.setattr("logic.sqlite3.connect", lambda _: original_connect(test_db))

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO professions_criteries (name, interests, education, income, work_type)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Программист", "Работа с техникой", "Высшее", "Высокий", "Офис"))
    conn.commit()
    conn.close()

    results = get_professions_by_criteria("Работа с техникой", "Высшее", "Высокий", "Офис")
    assert "Программист" in results


def test_get_profession_info(test_db, monkeypatch):
    original_connect = sqlite3.connect
    monkeypatch.setattr("logic.sqlite3.connect", lambda _: original_connect(test_db))

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Professions (name, category, description, responsibilities, advantages, disadvantages,
        average_salary, education_requirements, skills_required, career_prospects)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Программист", "IT", "Разработка ПО", "Кодирование", "Хорошая зарплата",
        "Много сидеть", 3000.00, "Высшее образование", "Python", "Рост до тимлида"
    ))
    conn.commit()
    conn.close()

    info = get_profession_info("Программист")
    assert info is not None
    assert "Программист" in info
    assert "IT" in info


