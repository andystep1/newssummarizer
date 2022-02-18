import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from functions import getsummary

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    await message.reply(f'Привет! {user_name}! Пришли мне новость')

@dp.message_handler()
async def start(message: types.Message):
    userinput = message.text
    await message.answer(getsummary(userinput))

if __name__ == '__main__': #всегда тру
    executor.start_polling(dp)