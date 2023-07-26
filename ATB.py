from os import getenv
from async_main import collect_data
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os


bot = Bot(token='')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Унікальні пропозиції від АТБ!']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Здоров козаче! '
                         'Заціни топ пропозицій АТБ', reply_markup=keyboard)  # greetings



@dp.message_handler(Text(equals='Унікальні пропозиції від АТБ!'))
async def ekb_city(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)


async def send_data(chat_id=''):
    file = await collect_data()
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
    await os.remove(file)


if __name__ == '__main__':
    executor.start_polling(dp)