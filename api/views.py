from curses.ascii import HT
from django.shortcuts import render,HttpResponse
from .models import Appointment
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/allAppointments/'},
        {'GET': '/api/appointment/id/'},
        {'POST': '/api/scheduleAppointment/'},
        {'PUT': '/api/appointment/id/'},
        {'DELETE': '/api/appointment/id/'},
       

        {'POST': '/api/token/'},
        {'POST': '/api/token/refresh/'},
    ]
    return Response(routes)



@api_view(['POST'])
def register(request):
    if request.method=='POST': # If the request is a POST request
        serializer = RegisterSerializer(data = request.data) # serialize the POST data
        data = {} # dictonary for generating access and refresh token when user is registered 
        if serializer.is_valid(): # checking for validation of serializer
            serializer.save() # save the changes to DataBase

            #generating output when user will be registered
            data['response'] = "Registration Successful" 
            data['username'] = request.data['username'] 
            data['email'] = request.data['email']
            refresh = RefreshToken.for_user(User)
            data['token'] = {
                'refresh': str(refresh), #getting refresh token
                'access': str(refresh.access_token), #getting access token
            }

        else:
           data = serializer.errors  #if serializer is not valid generating errors

        return Response(data) # getting Response as a Output
    