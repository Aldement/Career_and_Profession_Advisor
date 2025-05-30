import sqlite3


conn = sqlite3.connect("profession.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Professions (
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

professions = [
    # IT
    ('Программист', 'IT', 'Разработка программного обеспечения.', 'Написание и тестирование кода.', 'Высокая зарплата.', 'Долгое время за компьютером.', 3000.00, 'Высшее или курсы.', 'Языки программирования, логика.', 'Рост до архитектора ПО.'),
    ('Системный администратор', 'IT', 'Поддержка IT-инфраструктуры.', 'Настройка серверов и сетей.', 'Востребованность.', 'Ответственность за сбои.', 2500.00, 'Среднее или высшее образование.', 'Знание сетей и ОС.', 'Рост до IT-директора.'),
    ('Тестировщик ПО', 'IT', 'Тестирование программного обеспечения.', 'Поиск и документирование багов.', 'Хороший старт в IT.', 'Рутина.', 2200.00, 'Курсы или высшее образование.', 'Внимательность.', 'QA-лид.'),
    ('UX/UI дизайнер', 'IT', 'Проектирование пользовательского интерфейса.', 'Создание макетов и прототипов.', 'Творческая работа.', 'Требуется креатив.', 2800.00, 'Курсы.', 'Работа в Figma.', 'Арт-директор.'),
    ('Data Scientist', 'IT', 'Анализ данных и построение моделей.', 'Работа с большими данными.', 'Высокий спрос.', 'Сложность математики.', 4500.00, 'Высшее техническое.', 'Python, машинное обучение.', 'Главный аналитик.'),
    ('DevOps-инженер', 'IT', 'Автоматизация процессов разработки.', 'Настройка CI/CD.', 'Высокий доход.', 'Ответственность.', 4700.00, 'Техническое образование.', 'Linux, Docker.', 'Ведущий DevOps.'),

    # Медицина
    ('Врач', 'Медицина', 'Диагностика и лечение.', 'Приём пациентов.', 'Социальная значимость.', 'Высокая ответственность.', 4000.00, 'Медицинский вуз.', 'Медицинские знания.', 'Специализация, научная карьера.'),
    ('Фармацевт', 'Медицина', 'Выдача медикаментов.', 'Консультация клиентов.', 'Стабильная работа.', 'Монотонность.', 2000.00, 'Фармацевтическое образование.', 'Знание препаратов.', 'Рост до заведующего аптекой.'),
    ('Медсестра', 'Медицина', 'Уход за пациентами.', 'Выполнение назначений врача.', 'Помощь людям.', 'Эмоциональная нагрузка.', 2200.00, 'Медицинский колледж.', 'Навыки ухода за больными.', 'Старшая медсестра.'),
    ('Стоматолог', 'Медицина', 'Диагностика и лечение зубов.', 'Проведение процедур.', 'Высокий доход.', 'Длительное обучение.', 5000.00, 'Медицинский вуз.', 'Стоматология.', 'Открытие собственной клиники.'),

    # Образование
    ('Учитель', 'Образование', 'Обучение детей.', 'Проведение уроков.', 'Отпуск летом.', 'Эмоциональная нагрузка.', 1800.00, 'Педагогический вуз.', 'Педагогические навыки.', 'Рост до директора школы.'),
    ('Преподаватель вуза', 'Образование', 'Преподавание студентам.', 'Лекции и семинары.', 'Научная деятельность.', 'Нагрузка и отчётность.', 2500.00, 'Высшее образование и аспирантура.', 'Научные знания.', 'Профессорская степень.'),
    ('Воспитатель детсада', 'Образование', 'Уход за детьми.', 'Проведение занятий.', 'Работа с детьми.', 'Эмоциональная нагрузка.', 1600.00, 'Педагогическое образование.', 'Любовь к детям.', 'Заведующий детсадом.'),

    # Искусство и дизайн
    ('Графический дизайнер', 'Искусство', 'Создание визуальных концепций.', 'Разработка макетов.', 'Творческая работа.', 'Сложности с заказчиками.', 2200.00, 'Профильное образование.', 'Владение графическими редакторами.', 'Арт-директор.'),
    ('Фотограф', 'Искусство', 'Фотосъёмка мероприятий.', 'Редактирование снимков.', 'Творческая свобода.', 'Нерегулярный доход.', 1500.00, 'Курсы или самообучение.', 'Навыки фотосъёмки.', 'Собственное агентство.'),
    ('Иллюстратор', 'Искусство', 'Создание иллюстраций.', 'Рисование на заказ.', 'Творческая реализация.', 'Нестабильный доход.', 2000.00, 'Художественное образование.', 'Умение рисовать.', 'Работа с издательствами.'),
    ('Музыкант', 'Искусство', 'Исполнение музыки.', 'Участие в концертах.', 'Самовыражение.', 'Непредсказуемый доход.', 1800.00, 'Музыкальное образование.', 'Игра на инструментах.', 'Известный артист.'),
    ('Актер', 'Искусство', 'Игра в спектаклях и фильмах.', 'Участие в репетициях.', 'Творческая профессия.', 'Высокая конкуренция.', 2500.00, 'Театральное образование.', 'Актерское мастерство.', 'Главные роли.'),

    # Инженерия и производство
    ('Инженер-конструктор', 'Инженерия', 'Проектирование конструкций.', 'Создание чертежей.', 'Востребованность.', 'Ответственность за ошибки.', 3200.00, 'Инженерное образование.', 'Знание CAD.', 'Главный инженер.'),
    ('Электрик', 'Инженерия', 'Монтаж электросистем.', 'Прокладка кабеля.', 'Постоянный спрос.', 'Работа с риском.', 1800.00, 'Среднее спец.', 'Знание электрики.', 'Бригадир.'),
    ('Токарь', 'Инженерия', 'Обработка металлов.', 'Работа на станках.', 'Высокая точность.', 'Физическая нагрузка.', 1900.00, 'Профтехучилище.', 'Работа на станке.', 'Мастер участка.'),
    ('Сварщик', 'Инженерия', 'Сварка металлоконструкций.', 'Работа с оборудованием.', 'Высокая востребованность.', 'Опасность травм.', 2100.00, 'Среднее спец.', 'Навыки сварки.', 'Старший сварщик.'),

    # Строительство
    ('Архитектор', 'Строительство', 'Проектирование зданий.', 'Создание планов и макетов.', 'Творческая и аналитическая работа.', 'Ответственность за безопасность.', 3500.00, 'Архитектурный вуз.', 'Навыки проектирования.', 'Главный архитектор.'),
    ('Строитель', 'Строительство', 'Возведение зданий.', 'Работа на стройке.', 'Высокий спрос.', 'Физическая нагрузка.', 1700.00, 'Среднее проф.', 'Строительные навыки.', 'Прораб.'),
    ('Крановщик', 'Строительство', 'Управление башенным краном.', 'Перемещение грузов.', 'Высокий спрос.', 'Ответственность.', 2500.00, 'Профобразование.', 'Управление техникой.', 'Старший оператор.'),

    # Финансы и право
    ('Бухгалтер', 'Финансы', 'Финансовый учет.', 'Составление отчетности.', 'Стабильность.', 'Рутина.', 2400.00, 'Экономическое образование.', 'Знание налогового учета.', 'Финансовый директор.'),
    ('Аудитор', 'Финансы', 'Проверка финансовой отчетности.', 'Проведение аудиторских проверок.', 'Высокая востребованность.', 'Ответственность.', 3500.00, 'Финансовое образование.', 'Аналитические способности.', 'Партнер аудиторской фирмы.'),
    ('Юрист', 'Право', 'Правовая помощь.', 'Составление договоров.', 'Социальная значимость.', 'Высокая конкуренция.', 3000.00, 'Юридическое образование.', 'Знание законодательства.', 'Адвокатская практика.'),
    ('Нотариус', 'Право', 'Заверение документов.', 'Работа с клиентами.', 'Стабильный доход.', 'Требуется лицензия.', 4000.00, 'Юридическое образование.', 'Правовые знания.', 'Собственная контора.'),

    # Логистика и транспорт
    ('Водитель грузовика', 'Транспорт', 'Перевозка грузов.', 'Управление транспортом.', 'Свобода передвижения.', 'Долгие командировки.', 2800.00, 'Права категории C,E.', 'Внимательность.', 'Собственная логистическая компания.'),
    ('Логист', 'Транспорт', 'Организация доставки товаров.', 'Планирование маршрутов.', 'Высокий спрос.', 'Ответственность за задержки.', 2700.00, 'Экономическое или логистическое.', 'Аналитика и планирование.', 'Руководитель отдела логистики.'),
    ('Машинист поезда', 'Транспорт', 'Управление поездом.', 'Слежение за состоянием путей.', 'Хорошая зарплата.', 'Работа в праздники и выходные.', 3000.00, 'Специальное обучение.', 'Технические знания.', 'Старший машинист.'),
]

for profession in professions:
    cursor.execute('SELECT COUNT(*) FROM Professions WHERE name = ?', (profession[0],))
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO Professions (
                name, category, description, responsibilities, advantages, disadvantages,
                average_salary, education_requirements, skills_required,
                career_prospects
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', profession)

conn.commit()
conn.close()


conn = sqlite3.connect('profession.db')
cursor = conn.cursor()

# Создание таблицы для профессий
cursor.execute('''
    CREATE TABLE IF NOT EXISTS professions_criteries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        interests TEXT,
        education TEXT,
        income TEXT,
        work_type TEXT
    )
''')

categorized_professions = [
    # (Название, Интересы, Образование, Доход, Тип работы)

    # IT
    ('Программист', ['Работа с техникой', 'Научная работа'], ['Высшее', 'Курсы'], ['Средний', 'Высокий'], ['Удалённая', 'Офис']),
    ('Системный администратор', ['Работа с техникой'], ['Среднее специальное', 'Высшее'], ['Средний'], ['Офис']),
    ('Тестировщик ПО', ['Работа с техникой'], ['Курсы', 'Высшее'], ['Средний'], ['Офис', 'Удалённая']),
    ('UX/UI дизайнер', ['Творческая деятельность'], ['Курсы'], ['Средний'], ['Удалённая', 'Офис']),
    ('Data Scientist', ['Научная работа'], ['Высшее'], ['Высокий'], ['Офис', 'Удалённая']),
    ('DevOps-инженер', ['Работа с техникой'], ['Техническое образование'], ['Высокий'], ['Офис', 'Удалённая']),

    # Медицина
    ('Врач', ['Работа с людьми'], ['Высшее'], ['Высокий'], ['Офис']),
    ('Фармацевт', ['Работа с людьми'], ['Фармацевтическое образование'], ['Средний'], ['Офис']),
    ('Медсестра', ['Работа с людьми'], ['Среднее специальное'], ['Средний'], ['Офис']),
    ('Стоматолог', ['Работа с людьми'], ['Высшее'], ['Высокий'], ['Офис']),

    # Образование
    ('Учитель', ['Работа с людьми'], ['Высшее'], ['Низкий'], ['Офис']),
    ('Преподаватель вуза', ['Научная работа'], ['Высшее'], ['Средний'], ['Офис']),
    ('Воспитатель детсада', ['Работа с людьми'], ['Педагогическое образование'], ['Низкий'], ['Офис']),

    # Искусство и дизайн
    ('Графический дизайнер', ['Творческая деятельность'], ['Профильное образование'], ['Средний'], ['Удалённая', 'Офис']),
    ('Фотограф', ['Творческая деятельность'], ['Курсы', 'Не требуется'], ['Низкий'], ['Физический труд']),
    ('Иллюстратор', ['Творческая деятельность'], ['Художественное образование'], ['Средний'], ['Удалённая']),
    ('Музыкант', ['Творческая деятельность'], ['Музыкальное образование'], ['Низкий'], ['Физический труд']),
    ('Актер', ['Творческая деятельность'], ['Театральное образование'], ['Средний'], ['Физический труд']),

    # Инженерия и производство
    ('Инженер-конструктор', ['Работа с техникой'], ['Инженерное образование'], ['Средний'], ['Офис']),
    ('Электрик', ['Работа с техникой'], ['Среднее специальное'], ['Низкий'], ['Физический труд']),
    ('Токарь', ['Работа с техникой'], ['Профтехучилище'], ['Низкий'], ['Физический труд']),
    ('Сварщик', ['Работа с техникой'], ['Среднее специальное'], ['Средний'], ['Физический труд']),

    # Строительство
    ('Архитектор', ['Творческая деятельность'], ['Архитектурный вуз'], ['Высокий'], ['Офис']),
    ('Строитель', ['Работа с техникой'], ['Среднее специальное'], ['Низкий'], ['Физический труд']),
    ('Крановщик', ['Работа с техникой'], ['Профобразование'], ['Средний'], ['Физический труд']),

    # Финансы и право
    ('Бухгалтер', ['Работа с техникой'], ['Экономическое образование'], ['Средний'], ['Офис']),
    ('Аудитор', ['Работа с техникой'], ['Финансовое образование'], ['Высокий'], ['Офис']),
    ('Юрист', ['Работа с людьми'], ['Юридическое образование'], ['Средний'], ['Офис']),
    ('Нотариус', ['Работа с людьми'], ['Юридическое образование'], ['Высокий'], ['Офис']),

    # Логистика и транспорт
    ('Водитель грузовика', ['Работа с техникой'], ['Права категории C,E'], ['Средний'], ['Физический труд']),
    ('Логист', ['Работа с техникой'], ['Экономическое или логистическое образование'], ['Средний'], ['Офис']),
    ('Машинист поезда', ['Работа с техникой'], ['Специальное обучение'], ['Средний'], ['Физический труд']),
]

# Функция для вставки данных в таблицу
def insert_profession(name, interests, education, income, work_type):
    cursor.execute('''
        INSERT INTO professions_criteries (name, interests, education, income, work_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, ', '.join(interests), ', '.join(education), ', '.join(income), ', '.join(work_type)))
    conn.commit()

# Вставка данных
for profession in categorized_professions:
    cursor.execute('SELECT COUNT(*) FROM professions_criteries WHERE name = ?', (profession[0],))
    if cursor.fetchone()[0] == 0:
        insert_profession(*profession)

# Проверка, чтобы увидеть все данные
cursor.execute('SELECT * FROM professions_criteries')
conn.close()