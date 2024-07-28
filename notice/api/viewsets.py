from rest_framework import viewsets
from courses.views import get_token_user
from .serializers import NoticeSerializer, RecipientsSerializer
from ..models import Notice, Recipients
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from django.db.models import Q
from django.db.models import OuterRef, Subquery

class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return Notice.objects.all()
    
    @transaction.atomic
    def create(self, request):
        if isinstance(request.data, QuerySet):
            request.data._mutable=True
        
        token_user = get_token_user(self.request)
        request.data['created_by']=token_user.teacher.pk
        serializer = self.get_serializer(data=request.data)
        recipient_json = {}
        x=True if request.data['audience']!='All' else False
        if request.data['audience'] == 'Students':
            recipient_json['group'] = Group.objects.get(name='Students').pk
            recipient_json['course'] =request.data.get('course')
            recipient_json['shift'] =request.data.get('shift')
            recipient_json['semester'] =request.data.get('semester')
        
        if request.data['audience'] == 'Teachers':
            recipient_json['group'] = Group.objects.get(name='Teachers').pk
            
        if serializer.is_valid():
            print(serializer.validated_data)
            notice = serializer.save()
            
            if x:
                recipient_json['notice'] = notice.pk
                rs = RecipientsSerializer(data=recipient_json)  
                if rs.is_valid():
                    rs.save()          
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        print(serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['GET'], url_path='get-my-notices')
    def get_my_notices(self, request, *args, **kwargs):
        token_user = get_token_user(self.request)
        
        
        if request.headers['user']=='Teacher':
            notices = Notice.objects.filter(
                Q(audience='Teachers')|
                Q(audience='All')
            )
            
            return Response(
                NoticeSerializer(notices, many=True).data,
                status=status.HTTP_200_OK
            )
        
        if request.headers['user']=='Student':
            student = token_user.student
            students_only = Recipients.objects.filter(
                course=student.course,
                semester=student.semester,
                shift=student.shift
            ).values('notice')
            
            notices_queryset = Notice.objects.filter(
            Q(id__in=Subquery(students_only))|
            Q(audience='All')
            )
            print(notices_queryset)
            
            return Response(
                NoticeSerializer(notices_queryset, many=True).data
            )
        
        
        

@api_view(['GET'])
def get_all_events(request):
    notices = Notice.objects.filter(
        
    )
    
    