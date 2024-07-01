from rest_framework import viewsets
from courses.views import get_token_user
from .serializers import NoticeSerializer
from ..models import Notice
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.response import Response

class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return Notice.objects.all()
    
    def create(self, request):
        if isinstance(request.data, QuerySet):
            request.data._mutable=True
        
        token_user = get_token_user(self.request)
        request.data['created_by']=token_user.teacher.pk
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        print(serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    