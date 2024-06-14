from .serializers import *
from ..models import *
from rest_framework import viewsets

class AssignmentViewset(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    
    def get_queryset(self):
        return Assignment.objects.all()

class SubmissionViewset(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    
    def get_queryset(self):
        return Submission.objects.all()
    