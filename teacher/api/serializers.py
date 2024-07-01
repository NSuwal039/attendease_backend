from rest_framework import serializers

from courses.api.serializers import FacultySerializer
from ..models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    # user_info= serializers.SerializerMethodField()
    faculty_info = serializers.SerializerMethodField()
    
    # def get_user_info(self, obj):
    #     return CustomUserSerializer(obj.user).data

    
    def get_faculty_info(self, obj):
        return FacultySerializer(obj.faculty).data 
    class Meta:
        model = Teacher
        fields = '__all__'