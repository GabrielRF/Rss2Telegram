from bs4 import BeautifulSoup
from telebot import types
from time import gmtime
import feedparser
import os
import telebot
import time
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

def send_message(topic, button):
    MESSAGE_TEMPLATE = os.environ.get(f'MESSAGE_TEMPLATE', f'<b>{topic["title"]}</b>')

    btn_link = button
    if button:
        btn_link = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(f'{random.choice(EMOJIS.split(","))} {button}', url=topic['link'])
        btn_link.row(btn)

    if topic['photo']:
        response = requests.get(topic['photo'], headers = {'User-agent': 'Mozilla/5.1'})
        open('img', 'wb').write(response.content)
        photo = open('img', 'rb')
        for dest in DESTINATION.split(','):
            try:
                bot.send_photo(dest, photo, caption=MESSAGE_TEMPLATE, parse_mode='HTML', reply_markup=btn_link)
            except telebot.apihelper.ApiTelegramException:
                send_message(topic, False)
    else:
        for dest in DESTINATION.split(','):
            bot.send_message(dest, MESSAGE_TEMPLATE, parse_mode='HTML', reply_markup=button, disable_web_page_preview=True)
    print(f'... {topic["title"]}')
    time.sleep(0.2)

def get_img(url):
    response = requests.get(url, headers = {'User-agent': 'Mozilla/5.1'})
    try:
        html = BeautifulSoup(response.content, 'html.parser')
        photo = html.find('meta', {'property': 'og:image'})['content']
    except TypeError:
        photo = False
    return photo

def check_topics(url):
    now = gmtime()
    feed = feedparser.parse(url)
    try:
        source = feed['feed']['title']
    except KeyError:
        print(f'\nERRO: {url} não parece um feed RSS válido.')
        return
    print(f'\nChecando {source}:{url}')
    for tpc in reversed(feed['items'][:10]):
        topic = {}
        topic['site_name'] = feed['feed']['title']
        topic['title'] = tpc.title.strip()
        topic['summary'] = tpc.summary
        topic['link'] = tpc.links[0].href
        topic['photo'] = get_img(tpc.links[0].href)
        BUTTON_TEXT = os.environ.get(f'BUTTON_TEXT', False)
        send_message(topic, BUTTON_TEXT)
        add_to_history(topic['link'])

if __name__ == "__main__":
    for url in URL.split(','):
        check_topics(url)

