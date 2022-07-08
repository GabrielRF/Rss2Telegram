from bs4 import BeautifulSoup
from telebot import types
from time import gmtime
import os
import telebot
import random
import requests
import feedparser

URL = os.environ.get('URL')
DESTINATION = os.environ.get('DESTINATION')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
EMOJIS = os.environ.get('EMOJIS', '🗞 📰 🗒 🗓 📋 🔗 📝 🗃')

bot = telebot.TeleBot(BOT_TOKEN)

def send_message(title, link, photo):
    btn_link = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(f'{random.choice(EMOJIS.split())} Leia mais', url=link)
    btn_link.row(btn)
    print(f'Enviando {title}')
    try:
        response = requests.get(photo)
        open('img.png', 'wb').write(response.content)
        photo = open('img.png', 'rb')
        bot.send_photo(f'@{DESTINATION}', photo, caption=title, parse_mode='HTML', reply_markup=btn_link)
    except:
        bot.send_message(f'@{DESTINATION}', title, parse_mode='HTML', reply_markup=btn_link)

def get_img(url):
    response = requests.get(url, headers = {'User-agent': 'Mozilla/5.1'})
    html = BeautifulSoup(response.content, 'html.parser')
    return html.find('meta', {'property': 'og:image'})['content']

def check_topics(url):
    now = gmtime()
    feed = feedparser.parse(URL)
    for topic in reversed(feed['items'][:10]):
        pub_date = int(f'{topic.published_parsed[0]}{topic.published_parsed[1]:02}{topic.published_parsed[2]:02}')
        yesterday = int(f'{now[0]}{now[1]:02}{now[2]:02}') - 1
        if pub_date < yesterday:
            continue
        title = f'<b>{topic.title}</b>'
        link = topic.links[0].href
        photo = get_img(topic.links[0].href)
        if is_new(link):
            send_message(title, link, photo)

def get_history():
    response = requests.get(f'https://t.me/s/{DESTINATION}')
    if response.status_code != 200:
        return False
    return BeautifulSoup(response.content, 'html.parser')

def is_new(link):
    if link not in str(get_history()):
        return True
    return False

if __name__ == "__main__":
    for url in URL.split():
        print(f'Checando {url}...')
        check_topics(url)

