from aiogram import Bot, Dispatcher, executor, types
from random import randint
from aiogram.dispatcher.storage import FSMContext
import logging
import time

ADMIN_ID = 5735462741  #  свой ID


API_TOKEN = '8263535197:AAEnyQVmQHoz9Zq5-NUECLhfy79xcb7xtPU'

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['stop'], user_id=ADMIN_ID)
async def stop_bot(message: types.Message):
    await message.answer("⏹️ Останавливаю бота...")
    # Элегантная остановка
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()
    exit(0)

# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id=message.from_user.id
    user_name=message.from_user.first_name
    user_full_name=message.from_user.full_name
    logging.info(f'{user_full_name}{user_id}{user_name}{time.asctime()}')
    await message.reply(f"Привет {user_name}")
#узнать информацию о себе
@dp.message_handler(commands=['id'])
async def send_full_info(message: types.Message):
    user = message.from_user
    text = f"""
👤 Информация о тебе:

🆔 ID: `{user.id}`
👤 Имя: {user.first_name}
📛 Фамилия: {user.last_name or 'не указана'}
📛 Username: @{user.username or 'не указан'}
💬 ID чата: `{message.chat.id}`
    """
    await message.reply(text, parse_mode="Markdown")


#  /help  
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = """
Помощь по командам:
/start - начать
/help - помощь
/about - о боте
/number - случайное число от 1 до 100
/id - узнать всю инфу о себе
    """
    await message.reply(help_text)

@dp.message_handler(commands=['number'])
async def send_number(message: types.Message):
    number = randint(1, 100)
    await message.reply(str(number))
    
@dp.message_handler(commands=['about'])
async def send_number(message: types.Message):
    about="""
    Этот бот был создан экспеременатльно для тестирования функций aiogramm
    если вы хотите узнать о командах напишите:
    /help
    
    """
    await message.reply(str(about))

# Обработчик обычных сообщений
@dp.message_handler()
async def echo(message: types.Message):
    if 'привет' in message.text.lower():
        await message.reply("И тебе привет! 😊")
    else:
        await message.reply("Я получил твое сообщение: " + message.text)

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен!")
    executor.start_polling(dp, skip_updates=True)