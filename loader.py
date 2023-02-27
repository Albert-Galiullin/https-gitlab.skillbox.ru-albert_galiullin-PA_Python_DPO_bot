
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
import requests
import json
# import time
# import datetime
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP



storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
RAPID_API_KEY = config.RAPID_API_KEY
city = ''
lst = []
borders = []
date_hotels = []

def lowprice(message):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": message, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    print('Проверка')
    data = json.loads(response.text)  # преобразуем в словарь - десериализация JSON

    # определяем  gaiaId центра города
    a = list(findkeys(data, 'gaiaId'))

    n_gaiaId = a[0][0]

    # определяем  по gaiaId близлежащие отели
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {'currency': 'USD',
               'eapid': 1,
               'locale': 'ru_RU',
               'siteId': 300000001,
               'destination': {
                   'regionId':  n_gaiaId
               },
               'checkInDate': {'day': date_hotels[0].day, 'month': date_hotels[0].month, 'year': date_hotels[0].year},
               'checkOutDate': {'day': date_hotels[1].day, 'month': date_hotels[1].month, 'year': date_hotels[1].year},
               'rooms': [{'adults': 1}],
               'resultsStartingIndex': 0,
               'resultsSize': 10,
               'sort': 'PRICE_LOW_TO_HIGH',
               'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
               }


    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    # print(response.text)
    data = json.loads(response.text)  # преобразуем в словарь - десериализация JSON
    with open('req.json', 'w') as file:
        json.dump(data, file, indent=4)
    a0 = set(findkeys2(data, 'id'))
    a0 = list(a0)
    a1 = []
    #
    # print(a0)
    # print(borders)

    if lst[0] == 'lp':
        a1 = sorted(a0, key=lambda x:x[3])
    elif lst[0] == 'hp':
        a1 = sorted(a0, key=lambda x:x[3], reverse=True)
    elif lst[0] == 'bi':
        for i in range(len(a0)):
            if a0[i][3] >= borders[0] and a0[i][3] <= borders[1] and a0[i][4] >= borders[2] and a0[i][4] <= borders[3]:
                a1.append(a0[i])
    a1 = a1[:int(lst[3])]
    return a1

def load_photo(a):
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    list_photo = []
    for i in range(len(a)):
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "propertyId": a[i][0]
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        data = json.loads(response.text)  # преобразуем в словарь - десериализация JSON

        b = [a[i][1]] + list(findkeys3(data, 'url'))

        list_photo.append(b)
    return list_photo


def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv], node['regionNames']['shortName']
        for j in node.values():
            for x in findkeys(j, kv):
                yield (x)

def findkeys2(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys2(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            try:
                yield node[kv], node['name'], node["propertyImage"]["image"]["url"], \
                    node["price"]["options"][0]["strikeOut"]["amount"], node["destinationInfo"]["distanceFromDestination"]["value"],node["mapMarker"]["latLong"]["latitude"], node["mapMarker"]["latLong"]["longitude"]
            except:
                print('', end='')
        for j in node.values():
            for x in findkeys2(j, kv):
                yield (x)

def findkeys3(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys3(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys3(j, kv):
                yield (x)
