import sqlite3

from telegram import Update

insert_sql = 'INSERT INTO log (chat_id, username, full_name, message, response) VALUES (?, ?, ?, ?, ?)'

connection = sqlite3.connect('tbot.db', check_same_thread=False)
cursor = connection.cursor()

try:
    connection.execute('''CREATE TABLE `log` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `chat_id` INTEGER NOT NULL,
        `username` TEXT NOT NULL,
        `full_name` TEXT NOT NULL,
        `message` TEXT NOT NULL,
        `response` TEXT NOT NULL,
        `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );''')
    connection.execute('CREATE INDEX INDEX1 ON log (chat_id, created_at);')
except:
    print('Table already exists!')


def store_log(update: Update, response: str) -> None:
    try:
        cursor.execute(insert_sql, (
            update.message.chat.id,
            update.message.chat.username,
            update.message.chat.first_name + ' ' + update.message.chat.last_name,
            update.message.text,
            response
        ))
        connection.commit()
    except Exception as e:
        print(e)
