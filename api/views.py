from curses.ascii import HT
import datetime
from operator import itemgetter
from django.shortcuts import render,HttpResponse
from .models import Appointment
from .serializers import RegisterSerializer, AppointmentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.   

def Checker(Validated_data):
    user_start_time,user_end_time,user_date,user_id = Validated_data
    if (user_start_time > user_end_time):
        return False

    appointment = Appointment.objects.filter(guest=user_id)
    if len(appointment) == 0:
        return True

    valid_count=0
    for guest in appointment:
        if ((user_start_time < guest.start_time and user_end_time<guest.start_time) or (user_start_time>guest.end_time and user_end_time>guest.end_time)) or (user_date>guest.date):
            valid_count+=1

    if len(appointment) == valid_count:
        return True

    return False


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/allAppointments/'},
        {'GET': '/api/appointment/id/'},
        {'POST': '/api/scheduleAppointment/'},
        {'PUT': '/api/appointment/id/'},
        {'DELETE': '/api/appointment/id/'},

        {'POST': '/api/register/'},

        {'POST': '/api/token/'},
        {'POST': '/api/token/refresh/'},
    ]
    return Response(routes)


@api_view(['POST'])
def sheduleAppointment(request):
    if request.method=='POST':
        serializer = AppointmentSerializer(data = request.data)
        if serializer.is_valid():
            check = Checker([serializer.validated_data['start_time'],serializer.validated_data['end_time'],serializer.validated_data['date'],serializer.validated_data['guest']])
            if check:
                serializer.validated_data['available'] = False
                serializer.save()
            else:
                return HttpResponse("Time is not correct")
            return Response(serializer.data) 
        else:
            return Response(serializer.errors)

@api_view(['GET'])
def upcomingAppointment(request):
    l = []
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    current_date = datetime.date.today()
    
    appointment = Appointment.objects.all()
    
    for guest in appointment:    
        if current_time <= guest.start_time.strftime("%H:%M:%S") or current_date < guest.date:
            l.append({"title":guest.title,"agenda":guest.agenda,"start_time":guest.start_time,"end_time":guest.end_time,"date":guest.date})

    data = {}
    data['upcomingAppointment'] = l

    return Response(data)



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
    