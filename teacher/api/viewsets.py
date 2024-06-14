from rest_framework import viewsets
from .serializers import TeacherSerializer
from ..models import *
from authorization.api.serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

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
        
        teacher_json = {
            'teacher_code': request.data['teacher_code'],
            'address': request.data['address'],
            'contact': request.data['contact'],
            'user': user.pk,
            'faculty': request.data['faculty']
        }
        
        teacher_serializer = serializer(data=teacher_json)
        teacher_serializer.is_valid(raise_exception=True)
        teacher_serializer.save()
        
        return Response(
            teacher_serializer.data,
            status=status.HTTP_201_CREATED
        )
    