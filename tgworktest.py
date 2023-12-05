import datetime
import pause
from pyrogram import Client, filters
from configparser import ConfigParser
import asyncpg
from loguru import logger
#Нужно создать файл config с вашими данными
config = ConfigParser()
config.read('config.ini')
api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')
#Данные вашей базы
host='***'
port='***'
database='***'
user="***"
password='***'

app = Client(name= 'my_account', api_id=api_id, api_hash=api_hash)

@app.on_message(filters=filters.me)
async def get_c(event, message):
    logger.add("message.log", format="{time} {message}")
    logger.info(message.text)
    if (message.text == "/users_today"):
        conn = await asyncpg.connect(host=host, port=port, database=database, user=user, password=password)
        result = await conn.fetchval(f"SELECT COUNT (*) FROM users WHERE DATE(reg_at) = '{datetime.date.today()}'")
        await app.send_message(chat_id=message.chat.id, text=result)


@app.on_message(filters=filters.private)
async def auto_answer(event, message):
    logger.add("message.log",format="{time}{message}")
    conn = await asyncpg.connect(host=host, port=port, database=database, user=user, password=password)
    result = await conn.fetchval(f"SELECT COUNT (*) FROM users WHERE user_id = '{message.chat.id}'")
    if ("Хорошего дня" in message.text):
        await conn.execute(f'''UPDATE users SET trig = {True}''')
    if result == 0:
        await conn.execute('''INSERT INTO users(user_id, trig, reg_at) VALUES($1, $2, $3)''', message.chat.id, False, datetime.datetime.now())
        text = "Добрый день!"
        await app.send_message(chat_id=message.chat.id, text=text)
        need_date_1 = datetime.datetime.now()+datetime.timedelta(minutes=10)
        pause.until(need_date_1)
        text = "Подготовила для вас материал"
        await app.send_message(chat_id=message.chat.id, text=text)
        await app.send_photo(chat_id=message.chat.id, photo='photo.jpg')
        need_date_2 = datetime.datetime.now() + datetime.timedelta(minutes=90)
        pause.until(need_date_2)
        need_date_3 = datetime.datetime.now() + datetime.timedelta(hours=2)
        pause.until(need_date_3)
        check_v = await conn.fetchval(f"SELECT trig FROM users WHERE user_id = '{message.chat.id}'")
        if (check_v != True):
            text = "Скоро вернусь с новым материалом!"
            await app.send_message(chat_id=message.chat.id, text=text)

app.run()