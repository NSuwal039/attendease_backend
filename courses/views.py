from django.shortcuts import render
from django.utils import timezone
import datetime
from courses.models import *
import pytz
from rest_framework.authtoken.models import Token

def get_today_day():
    today = datetime.date.today()
    day_of_week_str = today.strftime("%A")[:3].upper()

    return (day_of_week_str)

def get_current_class(shift):
    time_now = timezone.now()
    time_now = time_now.astimezone(pytz.timezone('Asia/Kathmandu'))
    try:
        current_period = Period.objects.filter(
            start_time__lte = time_now,
            end_time__gte = time_now,
            shift = shift
        )
    except Period.DoesNotExist:
        current_period = None
    
    print(current_period)
    today_day = get_today_day()
    
    current_class = None
    if current_period!=None:
        current_class = Class.objects.get(
                period = current_period,
                day = today_day
            )

    return current_class

def get_token_user(request):
    token = request.headers['authorization'].split(' ')[1]
    token_user = Token.objects.get(key = token).user
    return token_user