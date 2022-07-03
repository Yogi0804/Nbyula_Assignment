import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Appointment
from .serializers import RegisterSerializer, AppointmentSerializer, ProfileUpdateSerializer
from .utils.util import checkAppoinment


# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    """This function get all Routes

        :param request
        :returns: Response
    """
    routes = [
        {"GET": '/api/'},
        {'GET': '/api/allAppointments/'},
        {"GET": '/api/upcomingAppointment/'},
        {'POST': '/api/scheduleAppointment/'},
        {'POST': '/api/register/'},
        {'POST': '/api/UpdateProfile/'},
        {'POST': '/api/offHours/'},
        {"DELETE": '/api/deleteAppointment/id/'},

        {'POST': '/api/token/'},
        {'POST': '/api/token/refresh/'},
    ]
    return Response(routes)


@api_view(['POST'])
def sheduleAppointment(request):
    """This function shedule an Appointment

        :param request
        :raises: `ValidationError`
        :returns: Response
    """

    if request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        return Response(checkAppoinment(serializer=serializer))


@api_view(['GET'])
def upcomingAppointment(request):
    """This function get a upcoming Appointment

        :param request
        :raises: `ValidationError`
        :returns: Response
    """
    storeupcomingAppointment = []
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    current_date = datetime.date.today()

    appointment = Appointment.objects.all()

    for guest in appointment:
        if current_date < guest.date:
            storeupcomingAppointment.append(
                {"title": guest.title, "agenda": guest.agenda, "start_time": guest.start_time,
                 "end_time": guest.end_time, "date": guest.date})
        if current_date == guest.date:
            if current_time < guest.start_time.strftime("%H:%M:%S"):
                storeupcomingAppointment.append(
                    {"title": guest.title, "agenda": guest.agenda, "start_time": guest.start_time,
                     "end_time": guest.end_time, "date": guest.date})

    data = {}
    data['upcomingAppointment'] = storeupcomingAppointment

    return Response(data)


@api_view(['POST'])
def register(request):
    """This function register a user

        :param request
        :raises: `ValidationError`
        :returns: Response
    """

    if request.method == 'POST':  # If the request is a POST request
        serializer = RegisterSerializer(data=request.data)  # serialize the POST data
        data = {}  # dictonary for generating access and refresh token when user is registered
        if serializer.is_valid():  # checking for validation of serializer
            serializer.save()  # save the changes to DataBase

            # generating output when user will be registered
            data['response'] = "Registration Successful"
            data['username'] = request.data['username']
            data['email'] = request.data['email']

        else:
            data = serializer.errors  # if serializer is not valid generating errors

        return Response(data)  # getting Response as a Output


@api_view(['POST'])
def UpdateProfile(request):
    """This function Updates a user Profile

        :param request
        :raises: `ValidationError`
        :returns: Response
    """
    if request.method == "POST":
        serializer = ProfileUpdateSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Wrong password."]})

            if serializer.validated_data['new_password'] != serializer.validated_data['confirm_password']:
                return Response({"message": "new password and confirm password doesn't match"})
            # set_password also hashes the password that the user will get
            user.set_password(serializer.validated_data.get("new_password"))
            user.username = serializer.validated_data['username']

            user.save()
            response = {
                'status': 'success',
                'message': 'Username and Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors)


@api_view(['GET'])
def allAppointments(request):
    """This function get all Appointments

        :param request
        :raises: `ValidationError`
        :returns: Response
    """

    appointment = Appointment.objects.all()  # generating a queryset
    serializer = AppointmentSerializer(appointment, many=True)  # serialize appointment queryset
    return Response(serializer.data)  # return as response


@api_view(['POST'])
def offHours(request):
    """This function submit offHours for a user

        :param request
        :raises: `ValidationError`
        :returns: Response
    """
    if request.method == "POST":
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['Username'] = request.user
            serializer.validated_data['title'] = "offhours"
            serializer.validated_data['agenda'] = "offhours"

        return Response(checkAppoinment(serializer=serializer))


@api_view(['DELETE'])
def deleteAppointment(request, pk):
    """This function deletes an Appointment

        :param request and primary key:
        :returns: Response
    """
    data = {}
    if request.method == "DELETE":
        try:
            appointment = Appointment.objects.get(id=pk)
        except:
            return Response({"Error": "User Id does not exist"})
        appointment.delete()
        data['response'] = f"Deleted appointment Successfully"
        return Response(data)

    return Response(data)
