from rest_framework import viewsets

from courses.api.serializers import ClassSerializer, SubjectSerializer, TeacherSubjectConfigSerializer
from .serializers import TeacherSerializer
from ..models import *
from authorization.api.serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import pytz
from django.utils import timezone
from courses.views import get_today_day
from django.contrib.auth.models import Group 

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    
    def get_queryset(self):
        return Teacher.objects.all()

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
        teacher_json = {
            'teacher_code': request.data['teacher_code'],
            'address': request.data['address'],
            'contact': request.data['contact'],
            'user': user.pk,
            'faculty': int(request.data['faculty'])
        }
        
        print(teacher_json)
        teacher_serializer = serializer(data=teacher_json)
        teacher_serializer.is_valid(raise_exception=True)
        teacher_serializer.save()
        
        return Response(
            teacher_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['GET'], url_path='get-current-class')
    def get_current_class(self, request, *args, **kwargs):
        time_now = timezone.now()
        time_now = time_now.astimezone(pytz.timezone('Asia/Kathmandu'))
        # print(time_now)
        self_obj = self.get_object()
        print(get_today_day())
        print(time_now)

        try:
            current_class = Class.objects.get(
            day=get_today_day(),
            subject__teacher = self_obj,
            period__start_time__lte = time_now,
            period__end_time__gte = time_now,
            )
            return Response(
                ClassSerializer(current_class).data,
            status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {
                    'error':'Class Not Found.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['GET'], url_path='get-teacher-current-classes')
    def get_teacher_classes(self, request, *args, **kwargs):
        subjects = TeacherSubjectConfig.objects.filter(teacher=self.get_object())
        
        return Response(
            TeacherSubjectConfigSerializer(subjects, many=True).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['GET'], url_path='get-routine')
    def get_routine(self, requets, *args, **kwargs):
        teacher = self.get_object()
        
        classes = Class.objects.filter(
            subject__teacher = teacher
        )
        
        return Response(
            ClassSerializer(classes, many=True).data,
            status=status.HTTP_200_OK
        )
        