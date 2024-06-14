from django.db import models
from teacher.models import *
from attendease.choices import CATEGORY_CHOICES

# Create your models here.

class Notice(models.Model):
    created_on = models.DateField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='notice_images')
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)