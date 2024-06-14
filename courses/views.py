from django.shortcuts import render
from django.utils import timezone
import datetime
from courses.models import *

def get_today_day():
    today = datetime.date.today()
    day_of_week_str = today.strftime("%A")[:3].upper()

    return (day_of_week_str)

def get_current_class():
    time_now = timezone.now()
    try:
        current_period = Period.objects.get(
            start_time__lte = time_now,
            end_time__gte = time_now
        )
    except Period.DoesNotExist:
        current_period = Period.objects.none()
    today_day = get_today_day()
    
    current_classes = Class.objects.filter(
            period = current_period,
            day = today_day
        ) if current_period!=None else None

    return current_classes