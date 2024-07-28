from rest_framework import serializers
from ..models import Student, StudentSubjectConfig
from courses.api.serializers import CourseSerializer

class StudentSerializer(serializers.ModelSerializer):
    course_info = serializers.SerializerMethodField()
    
    def get_course_info(self, obj):
        return CourseSerializer(obj.course).data
    class Meta:
        model = Student
        fields = '__all__'

class StudentSubjectConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectConfig
        fields = '__all__'