from rest_framework import viewsets

from attendance.api.serializers import StudentAttendanceSerializer
from courses.views import get_token_user
from ..models import *
from rest_framework.decorators import action
from .serializers import *
import datetime
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from datetime import datetime
from django.db.models import Q
from rest_framework.decorators import api_view
from attendance.models import StudentAttendance

num_to_day = {
    0: 'MON',
    1: 'TUE',
    2: 'WED',
    3: 'THU',
    4: 'FRI',
    5: 'SAT',
    6: 'SUN'
}

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
    
    @action(detail=False, methods=['GET'], url_path='get-date-classes')
    def get_date_classes(self, request, *args, **kwargs):
        user = get_token_user(request)
        student = user.student
        
        date = request.query_params.get('date')
        day = datetime.strptime(date, '%Y-%m-%d')
        weekday = num_to_day[day.weekday()]
        
        classes = Class.objects.filter(
            subject__semester = student.semester,
            subject__course = student.course,
            subject__shift = student.shift,
            day = weekday,
        )
        classes = classes.filter(
            Q(group = student.group)|
            Q(group = '-')
        ).order_by('period__start_time')
        
        to_return = []
        
        for item in classes:
            to_add = {}
            to_add['id']=item.id
            to_add['subject'] = f'{item.period.start_time.strftime('%H:%M')}-{item.subject.subject.name} ({item.type})'
            to_return.append(to_add)
        
        print(to_return)
        
        return Response(
            to_return,
            status=status.HTTP_200_OK
        )
    
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
    

    
@api_view(['get'])
def search(request):
    teacher = get_token_user(request).teacher
    print(request.query_params)
    
    course = Course.objects.get(id=request.query_params.get('course'))
    semester = int(request.query_params.get('semester'))
    shift = request.query_params.get('shift')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    attendances = StudentAttendance.objects.filter(
        attendance_date__gte = start_date,
        attendance_date__lte = end_date,
        student__semester=semester,
        student__shift=shift,
        student__course=course,
        subject_class__subject__teacher=teacher
    )
    print(attendances)
    
    return Response(
        StudentAttendanceSerializer(attendances, many=True).data
    )
    pass

    
