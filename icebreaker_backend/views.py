import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gcm.models import get_device_model
from icebreaker_backend.models import  *


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
            record = {"name": my_phone.reg_id+my_phone.dev_id}
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
            temp = phone.send_message({'title' : body['from'], 'message' : body['message'], 'id': '21'})
            print temp
            return JsonResponse({'status':'true'})
        else:
            return JsonResponse({'status':'false'})
