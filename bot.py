from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from handlers import start_handler, weather_handler, subscribe_handler, unsubscribe_handler, rate_handler
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Register command handlers
dp.register_message_handler(start_handler, commands=['start'])
dp.register_message_handler(weather_handler, commands=['weather'])
dp.register_message_handler(subscribe_handler, commands=['subscribe'])
dp.register_message_handler(unsubscribe_handler, commands=['unsubscribe'])
dp.register_message_handler(rate_handler, commands=['rate'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)