from django.db import models
from django.core.exceptions import ValidationError
from attendease.choices import *
from authorization.models import CustomUser
# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=255)

class Course(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

class Subject(models.Model):
    name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=5)

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    teacher_code = models.CharField(max_length = 3)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)

class TeacherSubjectConfig(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    photo = models.ImageField(upload_to='teacher_images', null=True, blank=True)
    
    shift = models.CharField(max_length=3, choices=SHIFT_CHOICES)
    
    def __str__(self):
        return f'{self.course.name}-{self.semester}-{self.shift}-{self.subject.name}-{self.teacher.user}'
    
    
class Period(models.Model):
    shift = models.CharField(max_length=3, choices=SHIFT_CHOICES)
    period = models.IntegerField(choices= PERIODS_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def clean(self) -> None:
        if self.start_time >= self.end_time:
            raise ValidationError ('Start time cannot be greater than end time')
    
class Class(models.Model):
    day = models.CharField(max_length=3, choices=DAYS_CHOICES)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    subject = models.ForeignKey(TeacherSubjectConfig, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='Lec')
    group = models.CharField(max_length=1, choices=GROUP_CHOICES, default='-')
    
# class Assignment(models.Model):
#     created_on = models.DateField(auto_now_add=True)
#     submit_by = models.DateField()
#     file = models.FileField(upload_to='assignment_question', blank=True, null=True)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)
#     student = models.ManyToManyField(Student, through='SubmittedAssignment')

# class SubmittedAssignment(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='student_assignments')
#     grade = models.FloatField()
#     feedback = models.TextField()
#     date_submitted = models.DateTimeField(auto_now_add=True)
