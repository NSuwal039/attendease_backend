from rest_framework import viewsets
from .serializers import StudentSerializer
from ..models import Student
from courses.models import *
from authorization.api.serializers import CustomUserSerializer
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action
import pandas as pd
from rest_framework import status

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
        
        student_json = {
            'college_roll': request.data['college_roll'],
            'dob': request.data['dob'],
            'course': Course.objects.get(name=request.data['course']).pk,
            'shift': request.data['shift'],
            'semester':1,
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
        
        