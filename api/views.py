from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/allAppointments'},
        {'GET': '/api/appointment/id'},
        {'PUT': '/api/appointment/id'},

        {'POST': '/api/appointment/'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)