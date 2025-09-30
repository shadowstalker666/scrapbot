from aiogram import types
import requests
from config import WEATHER_API_KEY, EXCHANGE_RATE_URL
from bs4 import BeautifulSoup
import sqlite3
from config import EXCHANGE_RATE_URL






async def start_handler(message: types.Message):
    await message.reply("Привет! Я бот. Доступные команды: /weather [город], /subscribe, /unsubscribe, /rate")

async def weather_handler(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Пожалуйста, укажите город: /weather [город]")
        return
    city = args
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    resp = requests.get(url)
    if resp.status_code != 200:
        await message.reply("Не удалось получить погоду. Проверьте название города.")
        return
    data = resp.json()
    temp = data['main']['temp']
    feels = data['main']['feels_like']
    desc = data['weather'][0]['description']
    await message.reply(f"Погода в {city}:\nТемпература: {temp}°C\nОщущается как: {feels}°C\nСостояние: {desc}")



async def rate_handler(message: types.Message):
    try:
        response = requests.get(EXCHANGE_RATE_URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Находим все строки с валютами
        rows = soup.find_all('div', class_='currency-row')

        usd_rate = None
        for row in rows:
            if 'USD' in row.text:  # ищем строку с USD
                span = row.find('span', class_='value')
                if span:
                    usd_rate = span.get_text(strip=True)
                break

        if not usd_rate:
            await message.reply("Не удалось найти курс доллара на странице Минфина.")
            return

        await message.reply(f"Курс доллара к гривне: {usd_rate}")

    except Exception as e:
        await message.reply(f"Ошибка при получении курса: {e}")
        



async def subscribe_handler(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect("subscribers.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS subscribers (user_id INTEGER PRIMARY KEY)")
    cur.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    await message.reply("Вы подписались на ежедневную рассылку погоды в 9:00!")

async def unsubscribe_handler(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect("subscribers.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    await message.reply("Вы отписались от рассылки.")

async def rate_handler(message: types.Message):
    resp = requests.get(EXCHANGE_RATE_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    rate_tag = soup.find("div", class_="sc-1x32wa2-9")
    if rate_tag:
        rate = rate_tag.text.strip()
        await message.reply(f"Курс доллара к гривне: {rate}")
    else:
        await message.reply("Не удалось получить курс валют.")