from .serializers import *
from ..models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from courses.models import Teacher
from rest_framework.response import Response
from rest_framework import status

class AssignmentViewset(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    
    def get_queryset(self):
        return Assignment.objects.all()
    
    def create(self, request):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['GET'], url_path='get-teacher-assignments')
    def get_teacher_assignments(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(id=request.query_params.get('id'))
        
        assignments = Assignment.objects.filter(
            assigned_class__teacher = teacher
        )
        
        return Response(
            AssignmentSerializer(assignments, many=True).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['GET'], url_path='get-student-assignments')
    def get_student_assignments(self, request, *args, **kwargs):
        print('here')
        student = Student.objects.get(id=request.query_params.get('id'))
        
        assignments = Assignment.objects.filter(
            assigned_class__course = student.course,
            assigned_class__semester = student.semester,
            assigned_class__shift = student.shift,
            
        )
        print(assignments)
        
        return Response(
            AssignmentSerializer(assignments, many=True).data,
            status=status.HTTP_200_OK
        )

class SubmissionViewset(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    
    def get_queryset(self):
        return Submission.objects.all()
    