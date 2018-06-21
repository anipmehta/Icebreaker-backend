from __future__ import print_function
from __future__ import print_function
import json
import datetime
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gcm.models import get_device_model
from django.http import HttpResponse
from icebreaker_backend.forms import UploadFileForm
import time
from icebreaker_backend.models import *


@csrf_exempt
def testing(request):
    if request.method == 'POST':
        milli_sec = int(round(time.time() * 1000))
        print(milli_sec)
        Device = get_device_model()
        projects_donated = []
        # phone = Device.objects.get(dev_id='anip2')
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
            temp = phone.send_message({'title': body['from'], 'message': body['message'], 'id': body['id'], 'time':
                str(millis), 'type': body['type']},
                                      collapse_key=str(millis))
            # print(temp)
            return JsonResponse({'status': 'true', 'time': millis})
        except Device.DoesNotExist:
            return JsonResponse({'status': 'false'})

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = User.objects.get(enroll=body['enroll'])
        user.gender = body['gender']
        user.branch = body['branch']
        user.college = body['college']
        user.batch = body['batch']
        user.save()
        contacts = []
        for contact in user.contacts.all():
            contacts.append(contact.enroll)
        profile = {"id": user.pk, "enroll": user.enroll, "gender": user.gender, "branch": user.branch,
                   "college": user.college, "batch": user.batch,"contacts":contacts}
        return JsonResponse({"status": "created", "data": profile})


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
                print(block.enroll)
                blocked.append(data)
            return JsonResponse({'blocked': blocked}, safe=False)
        else:
            return JsonResponse({'status': 'error'})


@csrf_exempt
def random_chat(request):
    if request.method == 'POST':
        Device = get_device_model()
        body = json.loads(request.body)
        milli_sec = int(round(time.time() * 1000))
        user = User.objects.get(enroll=body['enroll'])
        user_profile = {"id": user.pk, "enroll": user.enroll, "gender": user.gender, "branch": user.branch,
                        "college": user.college, "batch": user.batch}
        if str(user.gender) == 'male':
            try:
                female = Random.objects.filter(gender='female').order_by('time').first()
                female_random = User.objects.get(enroll=female.enroll)
                female_profile = {"id": female_random.pk, "enroll": female_random.enroll,
                                  "gender": female_random.gender,
                                  "branch": female_random.branch,
                                  "college": female_random.college, "batch": female_random.batch}

                female_device = Device.objects.get(name=female_random.enroll)
                female_device.send_message(
                    {'title': user.enroll, 'message': 'We have found a match for you!!', 'id': 2, 'time':
                        str(milli_sec), 'type': 'random', 'profile': user_profile},
                    collapse_key=str(milli_sec))
                male_device = Device.objects.get(name=user.enroll)
                male_device.send_message(
                    {'title': female_random.enroll, 'message': 'We have found a match for you!!', 'id': 2, 'time':
                        str(milli_sec), 'type': 'random', 'profile': female_profile},
                    collapse_key=str(milli_sec))
                female.delete()
                return JsonResponse({"status": "found", "profile": None})

            except:
                new_random = Random(enroll=user.enroll,
                                    gender=user.gender,
                                    time=milli_sec
                                    )
                new_random.save()
                return JsonResponse({"status": "wait", "profile": None})
        elif str(user.gender) == 'female':
            try:
                male = Random.objects.filter(gender='male').order_by('time').first()
                male_random = User.objects.get(enroll=male.enroll)
                male_profile = {"id": male_random.pk, "enroll": male_random.enroll, "gender": male_random.gender,
                                "branch": male_random.branch,
                                "college": male_random.college, "batch": male_random.batch}
                male_device = Device.objects.get(name=male_random.enroll)
                male_device.send_message(
                    {'title': user.enroll, 'message': 'We have found a match for you!!', 'id': 2, 'time':
                        str(milli_sec), 'type': 'random', 'profile': user_profile},
                    collapse_key=str(milli_sec))
                female_device = Device.objects.get(name=user.enroll)
                female_device.send_message(
                    {'title': male_random.enroll, 'message': 'We have found a match for you!!', 'id': 2, 'time':
                        str(milli_sec), 'type': 'random', 'profile': male_profile},
                    collapse_key=str(milli_sec))
                male.delete()
                return JsonResponse({"status": "found", "profile": None})
            except:
                new_random = Random(enroll=user.enroll,
                                    gender=user.gender,
                                    time=milli_sec
                                    )
                new_random.save()
                return JsonResponse({"status": "wait", "profile": None})

    else:
        return JsonResponse({"status": "error", "profile": None})


@csrf_exempt
def search(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if User.objects.filter(enroll=body['search']) and User.objects.filter(enroll=body['sender']):
            contact_user = User.objects.get(enroll=body['search'])
            user = User.objects.get(enroll=body['sender'])
            contact = Contacts(
                enroll=contact_user.enroll
            )
            try:
                if user.contacts.filter(enroll=contact.enroll).count() == 0:
                    contact.save()
                    user.contacts.add(contact)
                    profile = {"id": contact_user.pk, "enroll": contact_user.enroll, "gender": contact_user.gender, "branch": contact_user.branch,
                               "college": contact_user.college, "batch": contact_user.batch, "status":contact_user.status}
                    return JsonResponse({'status': 'found', 'contact_status': contact_user.status,'profile' : profile})
                else:
                    return JsonResponse({'status': 'already'})
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
        return JsonResponse({'status': 'true'})
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
        return JsonResponse({'status': 'false'})


@csrf_exempt
def upload_pic(request, enroll):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            m = Picture()
            m.picture = form.cleaned_data['picture']
            m.save()
            # print(str(m.picture.storage.url))
            # print(m.picture.url)
            # enroll = str(m.picture.url).replace("images/uploads/","")
            # print(str(m.picture.path))
            # enroll.replace(".png",""))
            user = User.objects.get(enroll=enroll)
            # print(enroll)
            # Picture.objects.get(picture=m.picture))
            user.picture = Picture.objects.get(picture=m.picture)
            # user.picture.save()
            user.save()
            return JsonResponse({"status": "true"}, safe=False)
        else:
            return JsonResponse({"status": "false"}, safe=False)


@csrf_exempt
def show_image(request, enroll):
    if request.method == 'GET':
        # body = json.loads(request.body)
        # pic = Picture()
        user = User.objects.get(enroll=enroll)

        try:
            image_data = open(user.picture.picture.url, "rb").read()
        except:
            if user.gender == 'male':
                image_data = open("images/uploads/male.jpg")
            else:
                image_data = open("images/uploads/female.jpg")
        return HttpResponse(image_data, content_type="image/png")
        # return JsonResponse({"url":user.picture.picture.url})


@csrf_exempt
def verify(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if User.objects.filter(enroll=body['enroll']).count() > 0:
            user = User.objects.get(enroll=body['enroll'])
            contacts = []
            for contact in user.contacts.all():
                contacts.append(contact.enroll)
            profile = {"id": user.pk, "enroll": user.enroll, "gender": user.gender, "branch": user.branch,
                       "college": user.college, "batch": user.batch,'contacts':contacts}
            return JsonResponse({"status": "exist", "data": profile},
                                safe=False)
        else:
            user = User(
                enroll=body['enroll']
            )
            user.save()
            return JsonResponse({"status": "created"})
    else:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def edit(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            user = User.objects.get(enroll=body['enroll'])
        except:
            return JsonResponse({'status': 'false'})
        user.gender = body['gender']
        user.branch = body['branch']
        user.college = body['college']
        user.batch = body['batch']
        user.status = body['status']
        user.save()
        return JsonResponse({'status': 'true'})
