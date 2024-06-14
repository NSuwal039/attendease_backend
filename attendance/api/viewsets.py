from rest_framework import viewsets
from ..models import *
from .serializers import *
from student.models import Student
from rest_framework.decorators import action

class StudentAttendanceViewset(viewsets.ModelViewSet):
    serializer_class = StudentAttendanceSerializer
    
    def get_queryset(self):
        return StudentAttendance.objects.all()
    
    @action(detail=False, methods=['GET'], url_path='generate-report')
    def generate_report(self, request, *args, **kwargs):
        month = int(request.query_params.get('month'))
        course = request.query_params.get('course')
        subject = request.query_params.get('subject')
        semester = request.query_params.get('semester')
        shift = request.query_params.get('shift')
        
        attendances = StudentAttendance.objects.filter(
            attendance_date__month = month
        )
        pass

class LeaveViewset(viewsets.ModelViewSet):
    serializer_class = LeaveSerializer
    
    def get_queryset(self):
        return Leave.objects.all()

