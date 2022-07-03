from django.http import HttpResponse
import datetime
from api.models import Appointment


def Validator(Validated_data):
    """This function Validate time and date Field

        :param Validated_data: contains : start_time, end_time, date, id
        :raises: `ValidationError`
        :returns: Response
    """

    user_start_time,user_end_time,user_date,user_id = Validated_data # Extracting data

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    current_date = datetime.date.today() # Current Date
    
    if current_date == user_date:
        if current_time > user_start_time.strftime("%H:%M:%S"):
            return [False,{"ERROR":'Entered time is lesser than Current time'}]

    if current_date > user_date: # No past Date Allowed 
        return [False,{"ERROR":'Entered date is lesser than Current Date'}]

    if (user_start_time > user_end_time): # start time can't be less than end time 
        return [False, {"ERROR":'start_time is Greater Than end_time'}]

    appointment = Appointment.objects.filter(guest=user_id) # get all the appointment for a particular Guest
    if len(appointment) == 0: # if Fist appointment schedule with Guest
        return [True,None]

    valid_count=0 # number of valid date and time i.e without colliding
    colliding_start_time = 0 # colliding start time
    colliding_end_time = 0 # colliding end time
    for guest in appointment: # looping through appointment object
        if ((user_start_time < guest.start_time and user_end_time<=guest.start_time) or (user_start_time>=guest.end_time and user_end_time>guest.end_time)) or (user_date>guest.date):
            valid_count+=1
        else:
            colliding_start_time = guest.start_time
            colliding_end_time = guest.end_time
            break

    if len(appointment) == valid_count: # if no collision occur
        return [True,None]

    # if any one collision occur
    return [False,{"ERROR":f'Your start_time and end_time are colliding with These start_time: {colliding_start_time} end_time: {colliding_end_time}'}]


def checkAppoinment(serializer):
    """This function check appoinments are valid or not

        :param serializer
        :raises: `ValidationError`
        :returns: dictionary
    """
    if serializer.is_valid():
        check,error = Validator([serializer.validated_data['start_time'],serializer.validated_data['end_time'],serializer.validated_data['date'],serializer.validated_data['guest']])
        if error is not None:
            return error
        if check:
            serializer.validated_data['available'] = False
            serializer.save()
        
        return serializer.data 
    
    return serializer.errors