from rest_framework import viewsets

from courses.views import get_token_user
from ..models import *
from rest_framework.decorators import action
from .serializers import *
import datetime
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

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
    
class TeacherSubjectConfigViewset(viewsets.ModelViewSet):
    serializer_class = TeacherSubjectConfigSerializer
    
    def get_queryset(self):
        token_user = get_token_user(self.request)
        if not token_user.is_superuser:
            return TeacherSubjectConfig.objects.filter(teacher = token_user.teacher)
        return TeacherSubjectConfig.objects.all()
    
    @action(detail=False, methods=['GET'], url_path='get-subjects')
    def get_subjects(self, request, *args, **kwargs):
        course_object = Course.objects.get(id=request.query_params['course'])        
        semester = request.query_params['semester']
        
        subjects = TeacherSubjectConfig.objects.filter(course=course_object, semester=semester).values('subject')  
        subject_list = [Subject.objects.get(id=item['subject']) for item in subjects]
        print(subject_list)
        
        return Response(SubjectSerializer(subject_list, many=True).data, status=status.HTTP_200_OK)
    
