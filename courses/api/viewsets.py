from rest_framework import viewsets
from ..models import *
from rest_framework.decorators import action
from .serializers import *
import datetime
from rest_framework.response import Response

class FacultyViewset(viewsets.ModelViewSet):
    serializer_class = FacultySerializer
    
    def get_queryset(self):
        return Faculty.objects.all()

class CourseViewset(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        return Course.objects.all()
    
class SubjectViewset(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    
    def get_queryset(self):
        return Subject.objects.all()

class ClassViewset(viewsets.ModelViewSet):
    serializer_class = ClassSerializer
    
    def get_queryset(self):
        return Class.objects.all()
    
            
