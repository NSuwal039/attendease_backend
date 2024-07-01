from datetime import datetime
from rest_framework import viewsets
from .serializers import StudentSerializer, StudentSubjectConfigSerializer
from ..models import Student, StudentSubjectConfig
from courses.models import *
from courses.api.serializers import *
from authorization.api.serializers import CustomUserSerializer
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action
import pandas as pd
from rest_framework import status
from attendance.models import StudentAttendance
from django.contrib.auth.models import Group

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        return Student.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        
        user_json = {
            'username': request.data['username'],
            'password': request.data['password'],
            'email': request.data['email'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name']
        }
        
        user_serializer = CustomUserSerializer(data=user_json)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.groups.add(
            Group.objects.get(name='Teachers')
        )
        user.save()
        
        student_json = {
            'college_roll': request.data['college_roll'],
            'dob': request.data['dob'],
            # 'course': Course.objects.get(name=request.data['course']).pk,
            'course': request.data['course'],
            'shift': request.data['shift'],
            'semester':request.data['semester'],
            'contact': request.data['contact'],
            'user': user.pk
        }
        
        student_serializer = serializer(data=student_json)
        student_serializer.is_valid(raise_exception=True)
        student_serializer.save()
        
        return Response(
            student_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['GET'], url_path='upload-csv')
    def upload_csv(self, request, *args, **kwargs):
        file = request.FILES.get('student_info')
        df = pd.read_csv(file)
        
        serializer = self.get_serializer_class()
        results = []
        
        for index, row in df.iterrows():
        
            user_json = {
                'username': row['username'],
                'password': row['password'],
                'email': row['email'],
                'first_name': row['first_name'],
                'last_name': row['last_name']
            }
            
            user_serializer = CustomUserSerializer(data=user_json)
            if user_serializer.is_valid():
                user = user_serializer.save()
            else:
                results.append(
                    {
                        'errors': serializer.errors,
                        'row': row.to_dict(),
                        'index':index
                    }
                )
            
            student_json = {
                'college_roll': row['college_roll'],
                'dob': row['dob'],
                'course': Course.objects.get(name=row['course']).pk,
                'shift': row['shift'],
                'semester':1,
                'contact': row['contact'],
                'user': user.pk
            }
            
            student_serializer = serializer(data=student_json)
            if student_serializer.is_valid():
                student_serializer.save()
            else:
                results.append(
                    {
                        'errors': student_serializer.errors,
                        'row': row.to_dict(),
                        'index':index
                    }
                )
        
        return Response(
            results,
            status=status.HTTP_201_CREATED
        )        
        
class StudentSubjectConfigViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSubjectConfigSerializer
    
    def get_queryset(self):
        return StudentSubjectConfig.objects.all()
    
    @action(detail=False, methods=['GET'], url_path='get-student-list')
    def get_student_list(self, request, *args, **kwargs):
        self_obj = Class.objects.get(id=request.query_params['class_id'])
        course = self_obj.subject.course
        subject = self_obj.subject.subject
        semester = self_obj.subject.semester
        
        print(course.name, subject.name, semester)
        
        students = StudentSubjectConfig.objects.filter(
            subject = subject,
            student__semester = semester,
            student__course = course 
        ).values_list('student__user')
        print(students)
        users = [CustomUser.objects.get(id=item[0]) for item in students]
        
        student_list = []
        today = datetime.today().date()
        for item in users:
            attendance = None
            try:
                attendance = StudentAttendance.objects.get(
                    student = item.student,
                    attendance_date = today,
                    subject_class = self_obj
                )
            except:
                pass
            
            dict = {
                'id': item.student.id,
                'name': f'{item.first_name} {item.last_name}',
                'college_roll': item.student.college_roll,
                'status':attendance.status if attendance!=None else 'A'
            }
                
            student_list.append(dict)
                
            
        return Response(
            student_list
        )
    
    @action(detail=False, methods=['GET'], url_path='get-custom-student-list')
    def get_custom_student_list(self, request, *args, **kwargs):
        course = Course.objects.get(id=request.query_params['course_id'])
        
        students=Student.objects.filter(
            course=course,
            semester = int(request.query_params['semester'])
        )
        to_send = []
        for item in students:
            dict={
                'id':item.id,
                'name': f'{item.user.first_name} {item.user.last_name}',
                'college_roll': item.college_roll,
                'status': 'A'
            }
            to_send.append(dict)
        return Response(
            to_send,
            status=status.HTTP_200_OK
        )