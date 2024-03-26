import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def gateway(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        return HttpResponse("")
