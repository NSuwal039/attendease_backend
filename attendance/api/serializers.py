from rest_framework import serializers
from ..models import *
from datetime import datetime

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    
    def get_student_name(self, obj):
        return f'{obj.student.user.first_name} {obj.student.user.last_name}'
    
    def get_student_id(self, obj):
        return obj.student.college_roll
    
    def get_subject(self, obj):
        return obj.subject_class.subject.subject.name
    
    class Meta:
        model = StudentAttendance
        fields = '__all__'
        
class LeaveSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()
    shift = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    
    def get_student_name(self,obj):
        return f'{obj.attendance.student.user.first_name} {obj.attendance.student.user.last_name}'
    
    def get_course(self,obj):
        return obj.attendance.student.course.name
    
    def get_semester(self,obj):
        return obj.attendance.student.semester
    
    def get_shift(self,obj):
        return obj.attendance.student.shift
    
    def get_date(self, obj):
        return obj.attendance.attendance_date.strftime('%Y-%m-%d')
    
    def get_subject(self, obj):
        return obj.attendance.subject_class.subject.subject.name
    
    def get_day(self, obj):
        return obj.attendance.subject_class.day
    
    
    
    class Meta:
        model = Leave
        fields = '__all__'

class CustomStudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomStudentAttendance
        fields = '__all__'