import json
import traceback

from django.core import serializers

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



def hello(request):
    return HttpResponse("Hello world ! ")
