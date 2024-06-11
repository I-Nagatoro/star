import sqlite3
import os
import json


def create_database():
    conn = sqlite3.connect('stars_and_constellations.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS constellations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            x_coordinate REAL NOT NULL,
            y_coordinate REAL NOT NULL,
            description TEXT,
            constellation_id INTEGER,
            size TEXT NOT NULL,
            FOREIGN KEY (constellation_id) REFERENCES constellations (id)
        )
    ''')

    conn.commit()
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect('stars_and_constellations.db')
    cursor = conn.cursor()

    constellations = [
        ('Орион', 'Выдающееся созвездие, видимое на всем земном шаре.'),
        ('Большая Медведица', 'Большое созвездие, известное благодаря содержащемуся в нем созвездию Большой Кар.'),
        ('Кассиопея',
         'Созвездие на северном небе, названное в честь тщеславной королевы Кассиопеи в греческой мифологии.'),
        ('Скорпион', 'Большое созвездие, расположенное около центра Млечного Пути.'),
        ('Лев', 'Созвездие зодиака, расположенное между Раком и Девой.'),
        ('Андромеда', 'Созвездие, названное в честь принцессы Андромеды в греческой мифологии.'),
        ('Лебедь', 'Северное созвездие на плоскости Млечного Пути.'),
        ('Телец', 'Большое и заметное созвездие на зимнем небосклоне северного полушария.'),
        ('Возничий', 'Созвездие северного полушария, часто ассоциируемое с мифическим возничим.'),
        ('Пегас', 'Созвездие, названное в честь крылатого коня Пегаса из греческой мифологии.'),
        ('Волопас', 'Созвездие северного полушария, содержащее яркую звезду Арктур.'),
        ('Геркулес', 'Большое созвездие, названное в честь героя Геракла из греческой мифологии.'),
        ('Малая Медведица', 'Созвездие, содержащее Полярную звезду.'),
        ('Дева', 'Созвездие зодиака, расположенное между Львом и Весами.'),
        ('Овен', 'Созвездие зодиака, расположенное между Рыбами и Тельцом.')
    ]

    cursor.executemany('''
        INSERT INTO constellations (name, description) VALUES (?, ?)
    ''', constellations)

    stars = [
        ('Бетельгейзе', 88.792939, 7.407064, 'Красный сверхгигант в созвездии Ориона.', 1, 'large'),
        ('Ригель', 78.634467, -8.201639, 'Голубой сверхгигант в созвездии Ориона.', 1, 'large'),
        ('Мизар', 200.981429, 54.925361, 'Двойная звездная система в рукоятке Большой Медведицы.', 2, 'medium'),
        ('Дубхе', 165.460415, 61.750832, 'Вторая по яркости звезда в созвездии Большой Медведицы.', 2, 'large'),
        ('Шедар', 10.126063, 56.537331, 'Звезда в созвездии Кассиопеи.', 3, 'medium'),
        ('Антарес', 247.351920, -26.432002, 'Самая яркая звезда в созвездии Скорпиона.', 4, 'large'),
        ('Регул', 152.092962, 11.967209, 'Самая яркая звезда в созвездии Льва.', 5, 'large'),
        ('Альфератц', 2.097096, 29.090431, 'Самая яркая звезда в созвездии Андромеды.', 6, 'medium'),
        ('Денеб', 310.357979, 45.280338, 'Голубой сверхгигант в созвездии Лебедя.', 7, 'large'),
        ('Альдебаран', 68.980162, 16.509302, 'Самая яркая звезда в созвездии Тельца.', 8, 'large'),
        ('Вега', 279.234734, 38.783688, 'Самая яркая звезда в созвездии Лиры.', 9, 'large'),
        ('Сириус', 101.287155, -16.716116, 'Самая яркая звезда ночного неба, находится в созвездии Большого Пса.', 10,
         'large'),
        ('Полярная звезда', 37.954560, 89.264108, 'Самая яркая звезда в созвездии Малой Медведицы.', 11, 'large'),
        ('Арктур', 213.915300, 19.182409, 'Самая яркая звезда в созвездии Волопаса.', 12, 'large'),
        ('Капелла', 79.172329, 45.997991, 'Самая яркая звезда в созвездии Возничего.', 13, 'large'),
        ('Процион', 114.825493, 5.224993, 'Вторая по яркости звезда в созвездии Малого Пса.', 14, 'medium'),
        ('Альтаир', 297.695827, 8.868322, 'Самая яркая звезда в созвездии Орла.', 15, 'large'),
        ('Спика', 201.298247, -11.161322, 'Самая яркая звезда в созвездии Девы.', 16, 'large'),
        ('YZ Кита', 23.507924, -7.790342, 'Малая красная звезда в созвездии Кита.', 17, 'small'),
        ('Глизе 581', 229.868201, -7.722013, 'Красный карлик в созвездии Весов, известен своей планетной системой.', 18,
         'small')
    ]
    cursor.executemany('''
        INSERT INTO stars (name, x_coordinate, y_coordinate, description, constellation_id, size) VALUES (?, ?, ?, ?, ?, ?)
    ''', stars)

    conn.commit()
    conn.close()


class Star:
    def __init__(self, id, name, x, y, description, constellation_id, size):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.description = description
        self.constellation_id = constellation_id
        self.size = size


class Constellation:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


def fetch_constellations_and_stars():
    conn = sqlite3.connect('stars_and_constellations.db')
    constellations = []
    stars = []

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM constellations")
    for row in cursor.fetchall():
        constellations.append(Constellation(row[0], row[1], row[2]))

    cursor.execute("SELECT id, name, x_coordinate, y_coordinate, description, constellation_id, size FROM stars")
    for row in cursor.fetchall():
        stars.append(Star(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    conn.close()
    return constellations, stars


def display_star_map(stars, symbols):
    os.system('cls' if os.name == 'nt' else 'clear')
    width, height = 80, 20

    for star in stars:
        x = int(star.x / 360 * width) % width
        y = int((90 - star.y) / 180 * height) % height
        symbol = symbols.get(star.size, '*')

        print(star.name.center(width))
        print("-" * width)
        sky = [[' ' for _ in range(width)] for _ in range(height)]
        sky[y][x] = symbol
        for row in sky:
            print(''.join(row))
        print("-" * width)


def display_star_details(stars, constellations):
    constellations_dict = {c.id: c for c in constellations}

    star_choice = input("Введите порядковый номер звезды или её название: ").strip()
    try:
        index = int(star_choice) - 1
        if 0 <= index < len(stars):
            selected_star = stars[index]
        else:
            print("Неверный номер звезды.")
            return
    except ValueError:
        selected_star = next((star for star in stars if star.name.lower() == star_choice.lower()), None)
        if not selected_star:
            print("Звезда не найдена.")
            return

    constellation = constellations_dict[selected_star.constellation_id]
    print(f"\nДетальная информация о звезде {selected_star.name}:")
    print(f"Название: {selected_star.name}")
    print(f"Описание: {selected_star.description}")
    print(f"Координаты: ({selected_star.x}, {selected_star.y})")
    print(f"Созвездие: {constellation.name}")
    print(f"Описание созвездия: {constellation.description}")


def load_symbols():
    try:
        with open('symbols.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'small': '.',
            'medium': '*',
            'large': 'O'
        }


def save_symbols(symbols):
    with open('symbols.json', 'w') as file:
        json.dump(symbols, file)


def main():
    create_database()
    insert_sample_data()

    constellations, stars = fetch_constellations_and_stars()
    symbols = load_symbols()

    while True:
        print("\nМеню:")
        print("1: Вывести карту неба")
        print("2: Вывести подробную информацию о звезде")
        print("3: Изменить символы отображения звёзд")
        print("4: Выйти")

        choice = input("\nВыберите опцию: ").strip()

        if choice == '4':
            break
        elif choice == '1':
            display_star_map(stars, symbols)
        elif choice == '2':
            display_star_details(stars, constellations)
        elif choice == '3':
            symbols['small'] = input("Введите символ для маленьких звезд: ").strip()
            symbols['medium'] = input("Введите символ для средних звезд: ").strip()
            symbols['large'] = input("Введите символ для больших звезд: ").strip()
            save_symbols(symbols)
        else:
            print("Неверная опция. Пожалуйста, выберите из предложенных опций.")


if __name__ == "__main__":
    main()
