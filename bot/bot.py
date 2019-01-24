#~/private/venvs/myvenv/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import vk_api
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import keyboards
from . import database as data
import os

key = keyboards.get_keyboards()
token = ''#your token

def auth():
    vk = vk_api.VkApi(token=token, api_version=5.68)
    vk._auth_token()
    return vk

def get_upload(vk):
    return vk_api.upload.VkUpload(vk)

def get_main_keyboard(id, connection):
    sql = "SELECT subscribe FROM USERS WHERE id = "+str(id)
    res = data.executeSQL(sql = sql, connection = connection)
    if res[0][0] == True:
        return key['main_menu_on']
    else:
        return key['main_menu_off']

def add_user(id, connection):
    sql = "SELECT id FROM USERS WHERE id = " + str(id)
    res = data.executeSQL(sql = sql, connection = connection)
    if res == 0:
        sql = "INSERT INTO USERS (id) VALUES("+str(id)+")"
        data.executeSQL(sql = sql, connection = connection)

def subscribe(id, vk, connection):
    sql = "SELECT subscribe FROM USERS WHERE id = " + str(id)
    res = data.executeSQL(sql, connection)
    if res[0][0]==False:
        sql = "UPDATE USERS SET subscribe = True WHERE id = "+str(id)
        data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Теперь я буду отправлять тебе новости о наших акциях и не только😉", "keyboard": get_main_keyboard(id, connection)})
    else:
        sql = "UPDATE USERS SET subscribe = False WHERE id = "+str(id)
        data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Если передумаешь, я буду рад🙃", "keyboard": get_main_keyboard(id, connection)})

def get_photos(directories, type, upload):
    files = []
    for directory in directories:
        allow_files = os.listdir(directory)
        if type == 'main':
            files.append(directory+"/"+allow_files[allow_files.index('main.jpeg')])
        else:
            for f in allow_files:
                files.append(directory+"/"+f)
    return upload.photo_messages(files)

def get_attachment(photos):
    attachment = ""
    for photo in photos:
        attachment = attachment + "photo"+str(photo['owner_id'])+"_"+str(photo['id'])+","
    return attachment[0:len(attachment)-1]

def get_auto_temp(state, connection):
    sql = ""
    if state[6] == "<10":
        sql = sql + "select mark, model, volume, drive_unit, steering, count_of_places, normal_price, img from CARS where"
    elif state[6] == "10-20":
        sql = sql + "select mark, model, volume, drive_unit, steering, count_of_places, good_price, img from CARS where"
    elif state[6] == ">20":
        sql = sql + "select mark, model, volume, drive_unit, steering, count_of_places, perfect_price, img from CARS where"
    if state[1]!=None:
        sql = sql + " type = '" + str(state[1]) + "'"
    else:
        sql = sql + " 1<2"
    return data.executeSQL(sql, connection)



def get_auto(state, connection):
    sql = ""
    if state[6] == "<10":
        sql = sql + "select mark, model, volume, drive_unit, steering, count_of_places, normal_price, img from CARS"
        if state[5] == "<2000":
            sql = sql + " where normal_price < 2000"
        elif state[5] == "2000-3000":
            sql = sql + " where normal_price >= 2000 and normal_price < 3000"
        elif state[5] == ">3000":
            sql = sql + " where normal_price >= 2000"
        else:
            sql = sql + " where 1<2"
    elif state[6] == "10-20":
        sql = sql + "select mark, model, volume, drive_unit, steering, count_of_places, good_price, img from CARS"
        if state[5] == "<2000":
            sql = sql + " where good_price < 2000"
        elif state[5] == "2000-3000":
            sql = sql + " where good_price >= 2000 and normal_price < 3000"
        elif state[5] == ">3000":
            sql = sql + " where good_price >= 2000"
        else:
            sql = sql + " where 1<2"
    elif state[6] == ">20":
        sql = sql + "select mark, model, volume, drive_unit, steering, count_of_places, perfect_price, img from CARS"
        if state[5] == "<2000":
            sql = sql + " where perfect_price < 2000"
        elif state[5] == "2000-3000":
            sql = sql + " where perfect_price >= 2000 and normal_price < 3000"
        elif state[5] == ">3000":
            sql = sql + " where perfect_price >= 2000"
        else:
            sql = sql + " where 1<2"
    if state[1]!=None:
        sql = sql + " and type = '" + str(state[1]) + "'"
    if state[2]!=None:
        sql = sql + " and drive_unit = '"+str(state[2])+"'"
    if state[3] == "<2":
        sql = sql+" and volume < 2"
    elif state[3] == "2-3":
        sql = sql +" and volume >= 2 and volume <3"
    elif state[3] == ">3":
        sql = sql +" and volume >=3"
    if state[4]!=None:
        sql = sql + " and steering = '"+str(state[4])+"'"
    return data.executeSQL(sql, connection)



def data_processing(id, pay, msg, vk, connection, upload):
    add_user(id = id, connection = connection)
    people = vk.method("users.get", {"user_ids":id})
    if pay=='"command":"start"' or pay == "admin":
        photos = get_photos(["/home/httpd/vhosts/chita-prokat.ru/httpdocs/static/bot/img/logo"], "main", upload)
        name = people[0]["first_name"]
        vk.method("messages.send", {"user_id": id, "message": "Привет, "+name+"!\nМеня зовут бот Макс. Я представляю лучшую компанию по аренде авто 'Прокат Сервис Чита'\n\nЯ могу рассказать тебе о компании, подобрать авто или показать список всех доступных авто!\n\nСо мной следует общаться посредством графической клавиатуры, это очень важно.\nИтак, начнем😎", "keyboard": get_main_keyboard(id = id, connection = connection), "attachment": get_attachment(photos)})
    elif msg=="admin":
        print('inside admin')
        vk.method("messages.send", {"user_id": id, "message": "Опять по новой? Ну, ладно...", "keyboard":key['start']})
    
    elif pay == "about":
        vk.method("messages.send", {"user_id": id, "message": "Какая информация Вас интересует?", "keyboard":key['about']})
    elif pay == "about_us":
        about = open("/home/httpd/vhosts/chita-prokat.ru/httpdocs/static/bot/info/about.txt", "rb")
        msg = about.read()
        vk.method("messages.send", {"user_id": id, "message": msg, "keyboard":get_main_keyboard(id = id, connection = connection)})
        about.close()
    elif pay == "about_rent":
        rent = open("/home/httpd/vhosts/chita-prokat.ru/httpdocs/static/bot/info/rent.txt", "rb")
        msg = rent.read()
        vk.method("messages.send", {"user_id": id, "message": msg})
        docs = open("/home/httpd/vhosts/chita-prokat.ru/httpdocs/static/bot/info/docs.txt", "rb")
        msg = docs.read()
        vk.method("messages.send", {"user_id": id, "message": msg, "keyboard":get_main_keyboard(id = id, connection = connection)})
        rent.close()
        docs.close()
    elif pay == "subscribe":
        subscribe(id, vk, connection)  
    elif pay == "selection":
        sql = "delete from USERS_CARS where id = "+str(id)
        data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Какой авто Вас интересует?", "keyboard": key['type']})
    elif pay == "how_long":
        if msg == "Минивэн":
            sql = "insert into USERS_CARS (id, type) values("+str(id)+", 'minivan')"
            data.executeSQL(sql, connection)
        elif msg == "Легковой авто":
            sql = "insert into USERS_CARS (id, type) values("+str(id)+", 'passenger')"
            data.executeSQL(sql, connection)
        elif msg == "Внедорожник":
            sql = "insert into USERS_CARS (id, type) values("+str(id)+", 'suv')"
            data.executeSQL(sql, connection)
        elif msg =="Неважно":
            sql = "insert into USERS_CARS (id) values("+str(id)+")"
            data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "На какой срок планируете брать авто? От этого зависит цена.", "keyboard": key['how_long']})
    
    elif pay == "finish_selection":
        if msg == "До десяти дней":
            sql = "update USERS_CARS set how_long = '<10' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От десяти до двадцати дней":  
            sql = "update USERS_CARS set how_long = '10-20' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От двадцати одного дня":
            sql = "update USERS_CARS set how_long = '>20' where id = "+str(id)
            data.executeSQL(sql, connection)
        sql = "select * from USERS_CARS where id = " + str(id)
        res = data.executeSQL(sql, connection)
        cars = get_auto_temp(res[0], connection)
        if cars != 0:
            i = 1
            s = ""
            directories = []
            #select mark, model, volume, drive_unit, steering, count_of_places, normal_price, img
            for car in cars:
                directories.append(car[7])
                s = s+str(i)+"."+str(car[0])+" "+str(car[1])+"\n"
                s = s+"Объем "+str(car[2])+" литра\n"
                if car[3] == "front":
                    s = s+"Передний привод\n"
                elif car[3] == "back":
                    s = s+"Задний привод\n"
                if car[4] == "left":
                    s = s+"Левый руль\n"
                elif car[4] == "right":
                    s = s+"Правый руль\n"
                s = s+str(car[5])+" мест\n"
                s = s+"Цена: "+str(car[6])+" рублей/день\n\n"
                i = i+1
                if i % 8 == 0:
                    photos = get_photos(directories, "main", upload)
                    vk.method("messages.send", {"user_id": id, "message":s, "attachment": get_attachment(photos)})
                    directories = []
                    s = ""
            if s != "":
                photos = get_photos(directories, "main", upload)
                vk.method("messages.send", {"user_id": id, "message":s, "attachment": get_attachment(photos)})
                vk.method("messages.send", {"user_id": id, "message":"Хотите, чтобы наш менеджер связался с Вами для уточнения информации по аренде автомобиля?\n\nОн напишет Вам в личные сообщения в самое ближайшее время.\n\nУбедитесь, что у Вас открыты личные сообщения.", "keyboard": key["connect"]})
        else:        
            vk.method("messages.send", {"user_id": id, "message": "К сожалению, по данным фильтрам результатов нет.", "keyboard": get_main_keyboard(id, connection)})     
    elif pay == "connect":
        if msg == "Да, хочу":
            fromaddr = "prokatservicechita@chita-prokat.ru"
            mypass = 'azsxdcfr132'
            toaddr = "prokatservicechita@gmail.com"
 
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Новый клиент!"
 
            m = "Пользователь vk.com/id"+str(id)+" хочет чтобы вы помогли ему с подбором:\n"
            sql = "select type from USERS_CARS where id = "+str(id)
            res = data.executeSQL(sql, connection)
            if res[0][0] == "suv":
                m = m + "Внедорожника\n"
            elif res[0][0] == "passenger":
                m = m + "Легового авто\n"
            elif res[0][0] == "minivan":
                m = m+"Минивэна\n"
            else:
                m = m+"Любого авто\n"
            sql = "select how_long from USERS_CARS where id = "+str(id)
            res = data.executeSQL(sql, connection)
            if res[0][0] == "<10":
                m = m + "Планирует брать на срок менее 10 дней"
            elif res[0][0] == "10-20":
                m = m + "Планирует брать на срок от 10 до 20 дней"
            elif res[0][0] == ">20":
                m = m + "Планирует брать на срок от 21 дня"
            msg.attach(MIMEText(m, 'plain'))
            server = smtplib.SMTP('smtp.chita-prokat.ru', 25) 
            server.starttls()
            server.login(fromaddr, mypass)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            vk.method("messages.send", {"user_id": id, "message": "С Ваши свяжутся в ближайшее время!", "keyboard": get_main_keyboard(id, connection)})
        elif msg == "Нет, спасибо":
            vk.method("messages.send", {"user_id": id, "message": "Как скажите", "keyboard": get_main_keyboard(id, connection)})
    else: 
        vk.method("messages.send", {"user_id":id, "message": "Я Вас не понимаю, используйте графическую клавиатуру!\n Если вы хотите узнать какую-либо информацию лично, пишите Максиму https://vk.com/mazzepa4x4","keyboard": get_main_keyboard(id = id, connection = connection)})