from django.db import models
from courses.models import Class, TeacherSubjectConfig
from student.models import Student

# Create your models here.

class Assignment(models.Model):
    created_on = models.DateField(auto_now_add=True)
    submit_by = models.DateField()
    file = models.FileField(upload_to='assignment_question', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_class = models.ForeignKey(TeacherSubjectConfig, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, through='Submission')

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to='student_assignments')
    grade = models.FloatField()
    feedback = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)