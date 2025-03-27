import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from dotenv import load_dotenv
import os

# Настройки
load_dotenv()  
BOT_TOKEN = os.getenv("BOT_TOKEN")  
API_URL = "https://api.thecatapi.com/v1/images/search"

# Создание бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создание клавиатуры
cat_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить котика"),
            KeyboardButton(text="Помощь")
        ],
        [
            KeyboardButton(text="О боте")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот с котиками \n"
        "Нажми кнопку ниже или напиши /cat",
        reply_markup=cat_keyboard
    )

# Обработчик команды /cat и кнопки "Получить котика"
@dp.message(Command("cat"))
@dp.message(lambda message: message.text == "Получить котика")
async def cmd_cat(message: types.Message):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            cat_data = response.json()
            cat_url = cat_data[0]['url']
            
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=cat_url,
                caption="Вот ваш случайный котик!",
                reply_markup=cat_keyboard
            )
        else:
            await message.answer(
                "Ой, не могу найти котиков(( Попробуйте позже!",
                reply_markup=cat_keyboard
            )
    
    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {e}",
            reply_markup=cat_keyboard
        )

# Обработчик кнопки "Помощь"
@dp.message(lambda message: message.text == "Помощь")
async def cmd_help(message: types.Message):
    await message.answer(
        "Как пользоваться ботом:\n"
        "- Нажмите 'Получить котика' для новой фотографии\n"
        "- Или используйте команду /cat\n\n"
        "Бот использует API thecatapi.com",
        reply_markup=cat_keyboard
    )

# Обработчик кнопки "О боте"
@dp.message(lambda message: message.text == "О боте")
async def cmd_about(message: types.Message):
    await message.answer(
        "Котобот v1.0\n\n"
        "Этот бот присылает случайные фото котиков.\n"
        "Разработано на Python с использованием aiogram.",
        reply_markup=cat_keyboard
    )

# Обработчик всех остальных сообщений
@dp.message()
async def other_messages(message: types.Message):
    await message.answer(
        "Я не понимаю эту команду \n"
        "Используйте кнопки ниже или команду /cat",
        reply_markup=cat_keyboard
    )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
