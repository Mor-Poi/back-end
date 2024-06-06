from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse

from db_connection import connect_mongodb
from ..test_serializers import TestSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


 
def get_one_booking(request):
    
    return HttpResponse("",content_type='application/json')

 
def update_booking(request):
    
    return HttpResponse("",content_type='application/json')

 
def delete_booking(request):
    
    return HttpResponse("",content_type='application/json')






