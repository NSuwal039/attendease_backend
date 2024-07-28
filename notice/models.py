from django.db import models
from teacher.models import *
from attendease.choices import CATEGORY_CHOICES
from attendease.choices import *
from django.contrib.auth.models import Group

# Create your models here.

class Notice(models.Model):
    created_on = models.DateField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    event_date_from = models.DateTimeField()
    event_date_to = models.DateTimeField(null=True, blank=True)
    audience = models.CharField(max_length=10)
    image = models.ImageField(upload_to='notice_images', null=True, blank=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Recipients(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)
    shift = models.CharField(max_length=3, choices=SHIFT_CHOICES, null=True, blank=True)
    