import logging
import os

from background import keep_alive
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from utils import query

load_dotenv()

API_TOKEN = os.environ['API_TOKEN']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
  """
    This handler will be called when user sends `/start` or `/help` command
    """
  await message.reply(
    "Welcome to Rechtsanwalt & Co! Your trusted partner in the realm of Swiss law. Whether you need assistance with litigation, tax planning, or company formation, our team of experts is always here to help."
  )


@dp.message_handler()
async def echo(message: types.Message):
  await message.answer("Just a sec, I'll reply...")
  await message.answer(query(message.text))


keep_alive()
if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
