import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gcm.models import get_device_model

from icebreaker_backend.forms import UploadFileForm
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
            record = {"name": my_phone.reg_id + my_phone.dev_id}
            projects_donated.append(record)
            # print temp
            # print type(temp)
        return JsonResponse({'name': projects_donated})


@csrf_exempt
def send(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        Device = get_device_model()
        if Device.objects.get(dev_id=body['to']) is not None:
            phone = Device.objects.get(dev_id=body['to'])
            temp = phone.send_message({'title': body['from'], 'message': body['message'], 'id': '21'})
            print temp
            return JsonResponse({'status': 'true'})
        else:
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
        body = json.loads(request.body)
        random = Random()
        user = User.objects.get(enroll=body['enroll'])
        print "kjjk"+user.gender
        print type(user.gender)
        if str(user.gender) == 'male':
            data = random.get_female()
            if str(data) == 'wait':
                random.insert_male(body['enroll'])
                return JsonResponse({'status': data})
            else:
                return JsonResponse({'status': data})
        elif str(user.gender) == 'female':
            data = random.get_male()
            if str(data) == 'wait':
                random.insert_female(body['enroll'])
                return JsonResponse({'status': data})
            else:
                return JsonResponse({'status': data})
        else:
            return JsonResponse({'status': 'error'})

    else:
        return JsonResponse({'status': 'error'})
