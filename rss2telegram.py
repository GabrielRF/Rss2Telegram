from bs4 import BeautifulSoup
from telebot import types
from time import gmtime
import feedparser
import os
import re
import telebot
import time
import random
import requests
import sqlite3

def get_variable(variable):
    if not os.environ.get(f'{variable}'):
        var_file = open(f'{variable}.txt', 'r')
        return var_file.read()
    return os.environ.get(f'{variable}')

URL = get_variable('URL')
DESTINATION = get_variable('DESTINATION')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
EMOJIS = os.environ.get('EMOJIS', '🗞,📰,🗒,🗓,📋,🔗,📝,🗃')
PARAMETERS = os.environ.get('PARAMETERS', False)
DRYRUN = os.environ.get('DRYRUN')

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
    if DRYRUN == 'failure':
        return
    MESSAGE_TEMPLATE = os.environ.get(f'MESSAGE_TEMPLATE', False)
    if MESSAGE_TEMPLATE:
        MESSAGE_TEMPLATE = set_text_vars(MESSAGE_TEMPLATE, topic)
    else:
        MESSAGE_TEMPLATE = f'<b>{topic["title"]}</b>'

    btn_link = button
    if button:
        btn_link = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(f'{button}', url=topic['link'])
        btn_link.row(btn)

    if topic['photo']:
        response = requests.get(topic['photo'], headers = {'User-agent': 'Mozilla/5.1'})
        open('img', 'wb').write(response.content)
        for dest in DESTINATION.split(','):
            photo = open('img', 'rb')
            try:
                bot.send_photo(dest, photo, caption=MESSAGE_TEMPLATE, parse_mode='HTML', reply_markup=btn_link)
            except telebot.apihelper.ApiTelegramException:
                topic['photo'] = False
                send_message(topic, button)
    else:
        for dest in DESTINATION.split(','):
            bot.send_message(dest, MESSAGE_TEMPLATE, parse_mode='HTML', reply_markup=button, disable_web_page_preview=True)
    print(f'... {topic["title"]}')
    time.sleep(0.2)

def get_img(url):
    try:
        response = requests.get(url, headers = {'User-agent': 'Mozilla/5.1'}, timeout=3)
        html = BeautifulSoup(response.content, 'html.parser')
        photo = html.find('meta', {'property': 'og:image'})['content']
    except TypeError:
        photo = False
    except requests.exceptions.ReadTimeout:
        photo = False
    return photo

def define_link(link, PARAMETERS):
    if PARAMETERS:
        if '?' in link:
            return f'{link}&{PARAMETERS}'
        return f'{link}?{PARAMETERS}'
    return f'{link}'



def set_text_vars(text, topic):
    cases = {
        'SITE_NAME': topic['site_name'],
        'TITLE': topic['title'],
        'SUMMARY': re.sub('<[^<]+?>', '', topic['summary']),
        'LINK': define_link(topic['link'], PARAMETERS),
        'EMOJI': random.choice(EMOJIS.split(","))
    }
    for word in re.split('{|}', text):
        try:
            text = text.replace(word, cases.get(word))
        except TypeError:
            continue
    return text.replace('\\n', '\n').replace('{', '').replace('}', '')


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
        if check_history(tpc.links[0].href):
            continue
        topic = {}
        topic['site_name'] = feed['feed']['title']
        topic['title'] = tpc.title.strip()
        topic['summary'] = tpc.summary
        topic['link'] = tpc.links[0].href
        topic['photo'] = get_img(tpc.links[0].href)
        BUTTON_TEXT = os.environ.get('BUTTON_TEXT', False)
        if BUTTON_TEXT:
            BUTTON_TEXT = set_text_vars(BUTTON_TEXT, topic)
        try:
            send_message(topic, BUTTON_TEXT)
        except telebot.apihelper.ApiTelegramException as e:
            print(e)
            pass
        add_to_history(topic['link'])

if __name__ == "__main__":
    for url in URL.split(','):
        check_topics(url)

