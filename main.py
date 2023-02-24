import json
import requests
import telebot
import datetime
import time
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from telebot import types

bot = telebot.TeleBot('5811515186:AAFNv4N4FxG3PKBEd0PoOkpN0sMLOExtDSU')
city = ''
lst = []
borders = []
date_hotels = []

@bot.message_handler(commands=['start'])
def start(message):
    mess = 'Привет, ' + message.from_user.first_name + '! Введи команду для поиска: /lowprice - топ самых дешёвых отелей в городе,' \
                                                       '/highprice  -топ самых дорогих отелей в городе, ' \
                                                       '/bestdeal  - топ отелей, наиболее подходящих по цене ' \
                                                       'и расположению от центра (самые дешёвые и находятся ближе всего к центру)'
    bot.send_message(message.from_user.id, mess, parse_mode='html')

@bot.message_handler(content_types=['text'])
def start(message):
    lst.clear()
    borders.clear()
    date_hotels.clear()
    if message.text == '/lowprice':
        lst.append('lp')
        lst.append(str(datetime.datetime.now()))
        bot.send_message(message.from_user.id, "Введи город:")
        bot.register_next_step_handler(message, get_city)
    elif message.text == '/highprice':
        lst.append('hp')
        lst.append(str(datetime.datetime.now()))
        bot.send_message(message.from_user.id, "Введи город:")
        bot.register_next_step_handler(message, get_city)
    elif message.text == '/bestdeal':
        lst.append('bi')
        lst.append(str(datetime.datetime.now()))
        bot.send_message(message.from_user.id, "Введи город:")
        bot.register_next_step_handler(message, get_city)
    elif message.text == '/history':
        try:
            with open('history.log', 'r', encoding='utf-8') as file:
                data_his = file.read()
            bot.send_message(message.from_user.id, data_his)
        except IOError:
            bot.send_message(message.from_user.id, 'Истории пока нет')
    elif message.text == '/help':
        mess = 'Привет, ' + message.from_user.first_name + '! Введи команду для поиска: /lowprice - топ самых дешёвых отелей в городе,' \
                                                           '/highprice  -топ самых дорогих отелей в городе, ' \
                                                           '/bestdeal  - топ отелей, наиболее подходящих по цене ' \
                                                           'и расположению от центра (самые дешёвые и находятся ближе всего к центру)'
        bot.send_message(message.from_user.id, mess, parse_mode='html')
    else:
        bot.send_message(message.from_user.id, 'Введите команду')


def get_city(message):

    city = message.text
    lst.append(city)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.from_user.id, 'Укажи дату въезда', parse_mode='html')
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
       mes = bot.edit_message_text(f"Select {LSTEP[step]}",
                             c.message.chat.id,
                             c.message.message_id,
                             reply_markup=key)

    elif result:
       mes = bot.edit_message_text(f"Выбор даты:  {result}",
                             c.message.chat.id,
                             c.message.message_id)
       date_hotels.append(result)
       print(lst)
       mes = bot.send_message(c.from_user.id, 'Введи количество дней проживания', parse_mode='html')

       bot.register_next_step_handler(mes, get_price)

@bot.message_handler(content_types=['text'])
def get_price(message):
    date_out = date_hotels[0] + datetime.timedelta(days=int(message.text))
    date_hotels.append(date_out)
    date_hotels.append(int(message.text))
    print(date_hotels)
    if lst[0] == 'bi':
        bot.send_message(message.from_user.id, "Введи нижнюю границу цены:")
        bot.register_next_step_handler(message, get_low_price)
    else:
        bot.send_message(message.from_user.id, "Введи количество отелей для выгрузки:")
        bot.register_next_step_handler(message, get_am_hotels)

def get_low_price(message):
    l_p = message.text
    borders.append(int(l_p))
    bot.send_message(message.from_user.id, "Введи верхнюю границу цены:")
    bot.register_next_step_handler(message, get_high_price)

def get_high_price(message):
    h_p = message.text
    borders.append(int(h_p))
    bot.send_message(message.from_user.id, "Введи минимальное расстояние до центра:")
    bot.register_next_step_handler(message, get_min_row)

def get_min_row(message):
    mi_r = message.text
    borders.append(int(mi_r))
    bot.send_message(message.from_user.id, "Введи максимальное расстояние до центра:")
    bot.register_next_step_handler(message, get_max_row)

def get_max_row(message):
    ma_r = message.text
    borders.append(int(ma_r))
    bot.send_message(message.from_user.id, "Введи количество отелей для выгрузки:")
    bot.register_next_step_handler(message, get_am_hotels)

def get_am_hotels(message):
    am_hotels = message.text
    lst.append(am_hotels)
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, "Фотографии отелей нужны?", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
@bot.callback_query_handler(func=lambda call: True)
def get_photo(call):
    lst.append(call.data)
    if call.data == "yes":
        mes = bot.send_message(call.from_user.id, 'Сколько фотографий загрузить по каждому отелю?')
        bot.register_next_step_handler(mes, get_photo_amount)
    else:
        a1 = lowprice(lst[2])
        if len(a1) > 0:
            answer = ''

            if int(lst[3]) < len(a1):
                cicle0 = int(lst[3])
            else:
                cicle0 = len(a1)

            for i in range(cicle0):
                answer += 'Отель: ' + a1[i][1] + ', Стоимость номера за ночь: ' + str(round(a1[i][3], 2)) + \
                          ' Стоимость номера за период: ' + str(date_hotels[2] * round(a1[i][3], 2)) + \
                          ', Расстояние до центра: ' + str(a1[i][4]) + ', Широта: ' + str(a1[i][5]) + \
                          ', Долгота: ' + str(a1[i][6]) + '\n'

                with open('history.log', 'w', encoding='utf-8') as file:
                    info = '\nРежим запроса: ' + lst[0] + '\nВремя запроса ' + (lst[1])[:16] + '\n' + answer
                    file.write(info)

            print(answer)
            bot.send_message(call.from_user.id, answer, parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_photo_amount(message):
    lst.append(message.text)
    print(lst)
    a1 = lowprice(lst[2])
    if len(a1) > 0:
        answer = ''

        if int(lst[3]) < len(a1):
            cicle0 = int(lst[3])
        else:
            cicle0 = len(a1)

        for i in range(cicle0):
            answer += 'Отель: ' + a1[i][1] + ', Стоимость номера за ночь: ' + str(round(a1[i][3], 2)) + \
                      ' Стоимость номера за период: ' + str(date_hotels[2] * round(a1[i][3], 2)) + \
                      ', Расстояние до центра: ' + str(a1[i][4]) + ', Широта: ' + str(a1[i][5]) + \
                      ', Долгота: ' + str(a1[i][6]) + '\n'

        print(answer)

        with open('history.log', 'w', encoding='utf-8') as file:
            info = '\nРежим запроса: '+ lst[0] + '\nВремя запроса ' + lst[1] + '\n'+answer
            file.write(info)

        bot.send_message(message.from_user.id, answer, parse_mode='html')
        bot.send_message(message.from_user.id, 'Подождите, загружается информация...', parse_mode='html')
        bot.send_message(message.from_user.id, 'Название отеля + карта с его местопооложением + фотографии отеля:', parse_mode='html')
        lst2 = load_photo(a1)



        for i in range(cicle0):
            if int(lst[5]) < len(lst2[i]) - 2:
                cicle = int(lst[5]) + 2
            else:
                cicle = len(lst2[i])
            for j in range(cicle):
                bot.send_message(message.from_user.id, lst2[i][j])
    else:
        bot.send_message(message.from_user.id, 'К сожалению, по указанным фильтрам ничего не найдено', parse_mode='html')

def lowprice(message):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": message, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    headers = {
        "X-RapidAPI-Key": "537090d3f5msh85dc7d5dad03ed7p13abffjsn13a4aa3a0315",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)  # преобразуем в словарь - десериализация JSON

    # определяем  gaiaId центра города
    a = list(findkeys(data, 'gaiaId'))
    print(data)
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
        "X-RapidAPI-Key": "537090d3f5msh85dc7d5dad03ed7p13abffjsn13a4aa3a0315",
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
            "X-RapidAPI-Key": "537090d3f5msh85dc7d5dad03ed7p13abffjsn13a4aa3a0315",
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



bot.polling(none_stop=True, interval=0)

