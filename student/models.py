from django.db import models
from authorization.models import CustomUser
from courses.models import *
from attendease.choices import SHIFT_CHOICES
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='student_images', null=True, blank=True)
    
    college_roll = models.TextField(max_length=10, unique=True)
    dob = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    shift = models.CharField(max_length=3, choices=SHIFT_CHOICES)
    semester = models.IntegerField()
    contact = models.CharField(max_length=10)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    
class StudentSubjectConfig(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    
    
    