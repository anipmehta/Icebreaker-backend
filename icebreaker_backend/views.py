import json

import datetime

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gcm.models import get_device_model

from icebreaker_backend.forms import UploadFileForm
import time
from icebreaker_backend.models import *


@csrf_exempt
def testing(request):
    if request.method == 'POST':
        Device = get_device_model()
        projects_donated = []
        # temp = Device.objects.all().send_message({'title': 'Hello Wolrd', 'message': 'my test message','notification':'hello'})
        phone = Device.objects.get(dev_id='anip2')
        # temp = phone.send_message({'title':'Hello Aditya','message': 'Hi From Anip','id': '25'}, collapse_key='something')
        # print temp
        for my_phone in Device.objects.all():
            # my_phone.send_message({'title': 'Hello World','message': 'my test message'}, collapse_key='something')
            record = {"name": my_phone.reg_id + my_phone.dev_id + "dev_name " + my_phone.name}
            projects_donated.append(record)
            # print temp
            # print type(temp)
        return JsonResponse({'name': projects_donated})


@csrf_exempt
def send(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        Device = get_device_model()
        now = datetime.datetime.now()
        millis = int(round(time.time() * 1000))
        try:
            phone = Device.objects.get(name=body['to'])
            temp = phone.send_message({'title': body['from'], 'message': body['message'], 'id': body['id'],'time':
                body['time'],'type': body['type']},
                                      collapse_key=str(millis))
            print temp
            return JsonResponse({'status': 'true'})
        except Device.DoesNotExist:
            return JsonResponse({'status': 'false'})


@csrf_exempt
def upload_pic(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            m = Picture()
            m.picture = form.cleaned_data['picture']
            m.save()
            return JsonResponse({'status': 'image upload success'})


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if User.objects.filter(enroll=body['enroll']).count() > 0:
            user = User.objects.get(enroll=body['enroll'])
            profile = {"id": user.pk, "enroll": user.enroll, "gender": user.gender, "branch": user.branch,
                       "college": user.college, "batch": user.batch}
            return JsonResponse({"status": "User updated", "data": profile},
                                safe=False)
        else:
            user = User(
                enroll=body['enroll'],
                gender=body['gender'],
                branch=body['branch'],
                college=body['college'],
                batch=body['batch'],
            )
            user.save()
            profile = {"id": user.pk, "enroll": user.enroll, "gender": user.gender, "branch": user.branch,
                       "college": user.college, "batch": user.batch}
            return JsonResponse({"status": "success", "data": profile})


@csrf_exempt
def block(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if User.objects.filter(enroll=body['user_enroll']).count() > 0:
            user = User.objects.get(enroll=body['user_enroll'])
            block = Blocked(enroll=body['block_enroll'])
            block.save()
            user.blocked.add(block)
            return JsonResponse({'status': 'Added to block list'})
        else:
            return JsonResponse({'status': 'error'})


@csrf_exempt
def block_list(request):
    body = json.loads(request.body)
    if request.method == 'POST':
        if User.objects.filter(enroll=body['enroll']).count() > 0:
            user = User.objects.get(enroll=body['enroll'])
            blocked = []
            for block in user.blocked.all():
                data = block.enroll
                print block.enroll
                blocked.append(data)
            return JsonResponse({'blocked': blocked}, safe=False)
        else:
            return JsonResponse({'status': 'error'})


@csrf_exempt
def random_chat(request):
    if request.method == 'POST':
        Device = get_device_model()
        body = json.loads(request.body)
        random = Random()
        user = User.objects.get(enroll=body['enroll'])
        if str(user.gender) == 'male':
            data = random.get_female()
            if str(data) == 'wait':
                random.insert_male(body['enroll'])
                return JsonResponse({'status': data})
            else:
                # phone1 = Device.objects.get(name=body['enroll'])
                # temp1 = phone1.send_message({'title': str(data), 'message': 'Hi, I want to chat with you', 'id': '21'})
                # print temp1
                # phone2 = Device.objects.get(name=data)
                # temp2 = phone2.send_message(
                #     {'title': body['enroll'], 'message': 'Hi, I want to chat with you', 'id': '21'})
                # print temp2
                return JsonResponse({'status': data})
        elif str(user.gender) == 'female':
            data = random.get_male()
            if str(data) == 'wait':
                random.insert_female(body['enroll'])
                return JsonResponse({'status': data})
            else:
                # phone1 = Device.objects.get(name=body['enroll'])
                # temp1 = phone1.send_message({'title': str(data), 'message': 'Hi, I want to chat with you', 'id': '21'})
                # print temp1
                # phone2 = Device.objects.get(name=data)
                # temp2 = phone2.send_message(
                #     {'title': body['enroll'], 'message': 'Hi, I want to chat with you', 'id': '21'})
                # print temp2
                return JsonResponse({'status': data})
        else:
            return JsonResponse({'status': 'error'})

    else:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def search(request):
    if request.method == 'POST':
        Device = get_device_model()
        body = json.loads(request.body)
        if User.objects.filter(enroll=body['search']) and User.objects.filter(enroll=body['sender']):
            contact = User.objects.get(enroll=body['search'])
            user = User.objects.get(enroll=body['sender'])
            contact = Contacts(
                enroll=contact.enroll
            )
            try:
                if user.contacts.filter(enroll=contact.enroll).count() == 0:
                    contact.save()
                    user.contacts.add(contact)
                    return JsonResponse({'status': 'found'})
                else:
                    return JsonResponse({'status' : 'already'})
            except IntegrityError:
                return JsonResponse({'status': 'already'})

        else:
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def delivered(request):
    if request.method == 'POST':
        Device = get_device_model()
        body = json.loads(request.body)
        millis = int(round(time.time() * 1000))
        try:
            phone = Device.objects.get(name=body['to'])
            temp = phone.send_message({'title': body['from'], 'message': True, 'id': body['id'], 'type': 'deliver'},
                                      collapse_key=str(millis))
        except Device.DoesNotExist:
            return JsonResponse({'status': 'false'})

    else:
        return JsonResponse({'status': 'false'})


@csrf_exempt
def removeRandom(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = User.objects.get(enroll=body['enroll'])
        random = Random()
        if str(user.gender) == 'male':
            random.slice_male(user.enroll)
        elif str(user.gender) == 'female':
            random.slice_female(user.enroll)
        return JsonResponse({'status': 'true'})
    else:
        return JsonResponse({'status':'false'})