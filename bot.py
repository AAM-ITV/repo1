import logging
from telegram import Update, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from bs4 import BeautifulSoup
import sqlite3

# Вставьте свой токен
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def create_connection():
    conn = sqlite3.connect('real_estate.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_listing(title, price, url):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO listings (title, price, url) VALUES (?, ?, ?)', (title, price, url))
    conn.commit()
    conn.close()

def get_listings():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT title, price, url FROM listings')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Создаем таблицу при первом запуске
create_table()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который поможет тебе найти недвижимость. Используй команду /search для поиска.')

def search(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Пожалуйста, укажите параметры поиска: Комнат, Цена, Город.')

def parse_avito(query_params):
    base_url = 'https://www.avito.ru/'
    search_url = f'{base_url}{query_params}'
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    listings = []
    for item in soup.find_all('div', class_='iva-item-root-Nj_hb'):
        title = item.find('h3').text
        price = item.find('span', class_='price-text-_YGDY').text
        url = item.find('a', class_='link-link-MbQDP').get('href')
        
        # Сохраняем результат в базу данных
        insert_listing(title, price, base_url + url)
        
        listings.append({'title': title, 'price': price, 'url': base_url + url})
    
    return listings

def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    params = user_input.split(',')
    query_params = {
        'rooms': params[0].strip(),
        'price': params[1].strip(),
        'city': params[2].strip()
    }

    # Пример параметров для Авито
    avito_query = f"{query_params['city']}?q={query_params['rooms']}+квартира+{query_params['price']}"
    parse_avito(avito_query)
    
    listings = get_listings()
    
    result_message = "Результаты поиска на Авито:\n\n"
    for listing in listings:
        result_message += f"Название: {listing[0]}\nЦена: {listing[1]}\nСсылка: {listing[2]}\n\n"

    update.message.reply_text(result_message, parse_mode=ParseMode.HTML)

def main
