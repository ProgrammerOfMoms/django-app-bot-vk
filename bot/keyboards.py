#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import json

def get_button(label, color,payload=""):
    return{
        "action":
        {
            "type":"text",
            "label": label,
            "payload":json.dumps(payload)
        },
        "color": color
    }
def convertToString(keyboard):
    return json.dumps(keyboard, ensure_ascii = False)

def get_keyboards():
    
    keyboard_start = {
        "one_time": True,
        "buttons":[
            [get_button(label="Начать",color="primary", payload="admin")]
        ]
    }
    keyboard_start = convertToString(keyboard_start)


    keyboard_main_menu_on = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Отписаться от новостей",color="default", payload="subscribe")
            ],
            [
                get_button(label="Узнать информацию",color="default", payload="about")
            ],
            [
                get_button(label="Подобрать авто",color="default", payload="selection")
            ]
        ]
    }
    keyboard_main_menu_on = convertToString(keyboard_main_menu_on)

    keyboard_main_menu_off = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Подписаться на новости",color="default", payload="subscribe")
            ],
            [
                get_button(label="Узнать информацию",color="default", payload="about")
            ],
            [
                get_button(label="Подобрать авто",color="default", payload="selection")
            ]
        ]
    }
    keyboard_main_menu_off = convertToString(keyboard_main_menu_off)

    keyboard_about = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="О компании",color="default", payload="about_us")
            ],
            [
                get_button(label="Об аренде",color="default", payload="about_rent")
            ],
        ]
    }
    keyboard_about = convertToString(keyboard_about)
    keyboard_type = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Легковой авто",color="default", payload="how_long") #drive_unit
            ],
            [
                get_button(label="Минивэн",color="default", payload="how_long")
            ],
            [
                get_button(label="Внедорожник",color="default", payload="how_long")
            ],
            [
                get_button(label="Неважно",color="default", payload="how_long")
            ]
        ]
    }
    keyboard_type = convertToString(keyboard_type)

    keyboard_drive_unit = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Передний",color="default", payload="volume")
            ],
            [
                get_button(label="Задний",color="default", payload="volume")
            ],
            [
                get_button(label="4wd",color="default", payload="volume")
            ],
            [
                get_button(label="Неважно",color="default", payload="volume")
            ]
        ]
    }
    keyboard_drive_unit = convertToString(keyboard_drive_unit)
    
    keyboard_volume = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="До двух литров",color="default", payload="steering")
            ],
            [
                get_button(label="От двух до трех литров",color="default", payload="steering")
            ],
            [
                get_button(label="От трех литров",color="default", payload="steering")
            ],
            [
                get_button(label="Неважно",color="default", payload="steering")
            ]
        ]
    }
    keyboard_volume = convertToString(keyboard_volume)

    keyboard_steering = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Левый",color="default", payload="price")
            ],
            [
                get_button(label="Правый",color="default", payload="price")
            ],
            [
                get_button(label="Неважно",color="default", payload="price")
            ]
        ]
    }
    keyboard_steering = convertToString(keyboard_steering)

    keyboard_price = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="До 2000 рублей/сутки",color="default", payload="how_long")
            ],
            [
                get_button(label="От 2000 до 3000 рублей/сутки",color="default", payload="how_long")
            ],
            [
                get_button(label="От 3000 рублей/сутки",color="default", payload="how_long")
            ],
            [
                get_button(label="Неважно",color="default", payload="how_long")
            ]
        ]
    }
    keyboard_price = convertToString(keyboard_price)

    keyboard_how_long = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="До десяти дней",color="default", payload="finish_selection")
            ],
            [
                get_button(label="От десяти до двадцати дней",color="default", payload="finish_selection")
            ],
            [
                get_button(label="От двадцати одного дня",color="default", payload="finish_selection")
            ]
        ]
    }
    keyboard_how_long = convertToString(keyboard_how_long)
    keyboard_connect = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Да, хочу",color="default", payload="connect")
            ],
            [
                get_button(label="Нет, спасибо",color="default", payload="connect")
            ]
        ]
    }
    keyboard_connect = convertToString(keyboard_connect)
    return {
        'start': keyboard_start,
        'main_menu_on': keyboard_main_menu_on,
        'main_menu_off':keyboard_main_menu_off,
        'about': keyboard_about,
        'type': keyboard_type,
        'drive_unit': keyboard_drive_unit,
        'volume': keyboard_volume,
        'steering': keyboard_steering,
        'price': keyboard_price,
        'how_long':keyboard_how_long,
        'connect': keyboard_connect
    }