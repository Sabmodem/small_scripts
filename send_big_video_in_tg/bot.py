from aiogram import Bot, Dispatcher, executor, types
from telethon import TelegramClient
import config
import os

api_token = os.environ.get('API_TOKEN')
bot_name = os.environ.get('BOT_NAME')
file_path = os.environ.get('FILE_PATH')
session_name = os.environ.get('SESSION_NAME')
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')

bot = Bot(token=api_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello world!")

@dp.message_handler(commands=['sendfile'])
async def sendfile(message: types.Message):
  async with TelegramClient(session_name, api_id, api_hash) as client:
    await client.send_file(bot_name, file_path)

@dp.message_handler(content_types=['document'])
async def echo(message: types.Message):
  await message.answer(message.document.file_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
