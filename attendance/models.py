from django.db import models
from student.models import *
from courses.models import *
from attendease.choices import ATTENDANCE_CHOICES, PERIODS_CHOICES
# Create your models here.


class Attendance(models.Model):
    # subject=models.ForeignKey(Subject,on_delete=models.DO_NOTHING, null=True)
    attendance_date=models.DateField()
    status = models.CharField(max_length = 50,choices = ATTENDANCE_CHOICES , blank=True, default='A')
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class StudentAttendance(Attendance):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_class = models.ForeignKey(Class, on_delete= models.CASCADE)

    attendance_by =models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Leave(models.Model):
    attendance = models.ForeignKey(StudentAttendance, on_delete= models.CASCADE)
    reason = models.TextField()
    status = models.BooleanField(default=False)

class CustomStudentAttendance(Attendance):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_by =models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    shift = models.CharField(max_length=3, choices=SHIFT_CHOICES)
    period = models.IntegerField(choices= PERIODS_CHOICES)
    
    class Meta:
        unique_together = ('attendance_date', 'shift', 'period', 'student')

    
