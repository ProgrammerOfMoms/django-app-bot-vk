# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from . import bot
import json

secret_key = ''#your secret key
group_id = 0#your group_id
access_string = ''#your access key


# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        if data['secret'] == secret_key:
            if data['type']=='confirmation' and data['group_id'] == group_id:
                return HttpResponse(access_string)
            elif data['type']=='message_new':
                if 'payload' in data['object']:
                    pay = data['object']['payload'][1:-1]
                else:
                    pay = 0
                msg = data['object']['body']
                user_id = data['object']['user_id']
                vk = bot.auth()
                connection = bot.data.connect()
                upload = bot.get_upload(vk)
                bot.data_processing(id = user_id, pay = pay, msg = msg, vk = vk, connection = connection, upload = upload)
                return HttpResponse('ok', content_type="text/plain", status=200)
            else:
                return HttpResponseNotFound('<h1>No Page Here</h1>')
        else:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
    else:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
