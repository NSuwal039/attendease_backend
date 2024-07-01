from rest_framework import viewsets
from ..models import *
from .serializers import *
from student.models import Student
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
import json

class StudentAttendanceViewset(viewsets.ModelViewSet):
    serializer_class = StudentAttendanceSerializer
    
    def get_queryset(self):
        return StudentAttendance.objects.all()
    
    def create(self, request):
        teacher = Teacher.objects.get(id=request.data['teacher_id'])
        class_obj = Class.objects.get(id=request.data['class_id'])
        
        attendances = []
        
        info = json.loads(request.data['attendance_info'])
        
        for item in info:
            x,created=StudentAttendance.objects.get_or_create(
                attendance_date = datetime.today().date(),
                student=Student.objects.get(id=item['student_id']),
                attendance_by = teacher,
                subject_class = class_obj
            )
            x.status = item['status']
            x.save()
            attendances.append(x)
        
        return Response(
            StudentAttendanceSerializer(attendances, many=True).data,
            status= status.HTTP_200_OK
        )
    
    def list(self, request):
        print(request.query_params)
        # class_obj = Class.objects.get(id=request.query_params['class_id'])
        # date = request.query_params['date']
        # date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        # date = date.date().isoformat()
        
        # attendances = StudentAttendance.objects.filter(
        #     subject_class = class_obj,
        #     attendance_date = date
        # )
        # print(attendances)
        
        # to_send = []
        
        # for item in attendances:
        #     x= {
        #         'name':f'{item.student.user.first_name} {item.student.user.last_name}',
        #         'status': item.status
        #     }
        #     to_send.append(x)
        
        # return Response(
        #     to_send,
        #     status=status.HTTP_200_OK
        # )
        # return Response(
        #     StudentAttendanceSerializer(attendances, many=True).data,
        #     status=status.HTTP_200_OK
        # )
        
        course=Course.objects.get(name=request.query_params['course'])
        semester=int(request.query_params['semester'])
        shift = 'Mor' if request.query_params['shift']=='Morning' else 'Day'
        from_date = request.query_params['from']
        from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S.%f')
        from_date_date = from_date.strftime('%Y-%m-%d')
        to_date = request.query_params['to']
        to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S.%f')
        to_date_date = to_date.strftime('%Y-%m-%d')
        
        x = StudentAttendance.objects.filter(
            student__course = course,
            student__semester = semester,
            student__shift = shift,
            attendance_date__gte = from_date,
            attendance_date__lte = to_date
        )
        for item in x:
            print (item.attendance_date, item.status, item.student.user)
        
        return Response({'a':'b'})
        
    
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

class CustomStudentAttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = CustomStudentAttendanceSerializer
    
    def get_queryset(self):
        return CustomStudentAttendance.objects.all()
    
    def create(self, request):
        print(request.data)
        teacher = Teacher.objects.get(id=request.data['teacher_id'])
        subject = Subject.objects.get(id=request.data['subject_id'])
        period = int(request.data['period'])
        shift = 'Mor' if request.data['shift']=='Morning' else 'Day'
        
        to_send=[]
        info = json.loads(request.data['attendance_info'])

        for item in info:
            x=CustomStudentAttendance.objects.create(
                attendance_date = datetime.today().date(),
                status = item['status'],
                student= Student.objects.get(id=item['student_id']),
                attendance_by=teacher,
                subject=subject,
                period=period,
                shift=shift
            )
            
            to_send.append(x)
        
        return Response(
            CustomStudentAttendanceSerializer(to_send, many=True).data,
            status=status.HTTP_200_OK
        )

