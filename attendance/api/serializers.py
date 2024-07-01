from rest_framework import serializers
from ..models import *

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'
        
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'

class CustomStudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomStudentAttendance
        fields = '__all__'