import sqlite3

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('users.db')

# Создаем курсор, чтобы выполнять запросы к базе данных
cursor = conn.cursor()

# Выполняем запрос к базе данных, чтобы получить всех пользователей
cursor.execute('SELECT * FROM users')

# Читаем все строки из результата запроса
rows = cursor.fetchall()

# Выводим данные на экран
for row in rows:
    print(f"{row[0]} - {row[1]}")

# Закрываем соединение с базой данных
conn.close()
