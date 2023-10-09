import os
import json
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.dispatcher.filters import Text
import openai
import sqlite3

openai.api_key = "YOUR_OPEN_AI_KEY"

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(bot)

#  база данных
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT)''')
conn.commit()


# Комадны
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    #  папка с именем пользователя
    folder_name = str(message.from_user.id)
    os.makedirs(folder_name, exist_ok=True)

    with open('images/sticker.gif', 'rb') as sticker:
        sticker = InputFile(sticker)
        await bot.send_animation(message.chat.id, sticker, caption=f'[~ZuckerAI~]\nПривет, {message.from_user.first_name}! 👤\nЯ Исскуственный интелект ThompSon AI\nИнтегрирован в платформу Telegram кодером K3RNEL-DEV\n[Доступные Команды]\n/help - Помощь\n/Автор - информация об Авторе\nТы можешь задать абсолютно любой вопрос нейросеть ответить тебе на него!')

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    with open('images/anonymous.gif', 'rb') as stick_help:
        sticker = InputFile(stick_help)
        await bot.send_animation(message.chat.id, sticker, caption=f'👤Name:{message.from_user.first_name}\n👁‍🗨Id:{message.chat.id}\n📕:Это интегрированный исскуственный интелект ThompSon AI в ней вы можете вводить любой интересующий вас вопрос и вы получаете ответ какой бы вопрос не-был сложным')


#Начало
@dp.message_handler(Text(equals=['Кто ты', 'кто ты', 'имя', 'как тебя зовут', 'Как тебя зовут', 'Кто тебя создал', 'Кто твой разработчик', 'кто тебя создал', 'твое имя' 'Твое Имя', 'а как тебя зовут', 'А как тебя зовут']))
async def who_are_you(message: types.Message):
    with open('images/about.gif', 'rb') as gif:
        gif_data = InputFile(gif)
        await bot.send_animation(message.chat.id, animation=gif_data, caption='Я Искусственный интелект ThompSon Ai\nСозданный на базе OPEN-AI и интегрирован в платформу-Telegram\nCreated by K3RNEL-DEV')


@dp.message_handler(text='/Автор')
async def who_am_i(message: types.Message):
    await message.reply(' **[~coder]\nИнтегрировано и модифицировано разработчиком K3rnel-Dev\nИскусственный интеллект на API  от OpenAI**', parse_mode=ParseMode.MARKDOWN)
#Конец


@dp.message_handler()
async def generate_text(message: types.Message):
    # Проверяем наличие username у пользователя
    user_id = message.from_user.id
    username = message.from_user.username
    if username is not None:
        # Сохраняем username в базу данных
        c.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()

    # Сохраняем сообщение пользователя в JSON-файл
    folder_name = str(user_id)
    file_name = os.path.join(folder_name, 'chat.json')
    with open(file_name, 'a') as f:
        json.dump({
            'user': user_id,
            'message': message.text,
            'bot_response': None
        }, f, ensure_ascii=False)

    # Генерируем ответ
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message.text}:",
        temperature=0.9,
        max_tokens=750,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    # Сохраняем ответ бота в JSON-файл
    with open(file_name, 'a') as f:
        json.dump({
            'user': None,
            'message': None,
            'bot_response': response.choices[0].text
        }, f, ensure_ascii=False)

    await message.reply(response.choices[0].text, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
