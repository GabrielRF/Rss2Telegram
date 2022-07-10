from bs4 import BeautifulSoup
from telebot import types
from time import gmtime
import feedparser
import os
import telebot
import random
import requests
import sqlite3

URL = os.environ.get('URL')
DESTINATION = os.environ.get('DESTINATION')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
EMOJIS = os.environ.get('EMOJIS', '🗞,📰,🗒,🗓,📋,🔗,📝,🗃')

bot = telebot.TeleBot(BOT_TOKEN)

def add_to_history(link):
    conn = sqlite3.connect('rss2telegram.db')
    cursor = conn.cursor()
    aux = f'INSERT INTO history (link) VALUES ("{link}")'
    cursor.execute(aux)
    conn.commit()
    conn.close()

def check_history(link):
    conn = sqlite3.connect('rss2telegram.db')
    cursor = conn.cursor()
    aux = f'SELECT * from history WHERE link="{link}"'
    cursor.execute(aux)
    data = cursor.fetchone()
    conn.close()
    return data

def send_message(source, title, link, photo):
    btn_link = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(f'{random.choice(EMOJIS.split(","))} {source}', url=link)
    btn_link.row(btn)
    print(f'Enviando {title}')
    try:
        response = requests.get(photo)
        open('img.png', 'wb').write(response.content)
        photo = open('img.png', 'rb')
        for dest in DESTINATION.split(','):
            bot.send_photo(dest, photo, caption=title, parse_mode='HTML', reply_markup=btn_link)
    except:
        for dest in DESTINATION.split(','):
            bot.send_message(dest, title, parse_mode='HTML', reply_markup=btn_link, disable_web_page_preview=True)

def get_img(url):
    response = requests.get(url, headers = {'User-agent': 'Mozilla/5.1'})
    html = BeautifulSoup(response.content, 'html.parser')
    return html.find('meta', {'property': 'og:image'})['content']

def check_topics(url):
    now = gmtime()
    feed = feedparser.parse(url)
    source = feed['feed']['title']
    print(f'Checando {source}...')
    for topic in reversed(feed['items'][:10]):
        title = f'<b>{topic.title}</b>'
        link = topic.links[0].href
        photo = get_img(topic.links[0].href)
        if not check_history(link):
            send_message(source, title, link, photo)
            add_to_history(link)
        else:
            print(f'Repetido: {link}')

if __name__ == "__main__":
    for url in URL.split(','):
        check_topics(url)

