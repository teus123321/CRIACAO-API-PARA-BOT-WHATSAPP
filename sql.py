import sqlite3

conexao = sqlite3.connect('banco.db', check_same_thread=False)
cursor = conexao.cursor()

def init_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        temp REAL NOT NULL,
        feels_like REAL NOT NULL,
        is_day INTEGER NOT NULL CHECK(is_day IN (0,1)),
        rain REAL NOT NULL,
        fetched_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    )
    ''')
    conexao.commit()


def insert_weather(lat: float, lon: float, temp: float, feels_like: float, is_day: bool, rain: float):
    cursor.execute('''
    INSERT INTO weather (latitude, longitude, temp, feels_like, is_day, rain)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (lat, lon, temp, feels_like, int(is_day), rain))
    conexao.commit()
    return cursor.lastrowid


def get_last_weather(lat: float, lon: float):
    cursor.execute('''
    SELECT id, latitude, longitude, temp, feels_like, is_day, rain, fetched_at
    FROM weather
    WHERE latitude = ? AND longitude = ?
    ORDER BY fetched_at DESC
    LIMIT 1
    ''', (lat, lon))
    return cursor.fetchone()
