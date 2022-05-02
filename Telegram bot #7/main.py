import logging
import config
from aiogram import Bot, Dispatcher, executor, types
import sqlite3

bot = Bot(token=config.BOT_KEY)
dp = Dispatcher(bot)

conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
try:
    cursor.execute("""
                    CREATE TABLE messages
                    (chat_id int, message_id integer, text text)
                """)
    cursor.execute("""
                    CREATE TABLE banWords
                    (word text)
                """)
except:
    pass


async def startup(dp):
    await bot.send_message(816283979, "Бот запущен")

if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=startup)