from rest_framework import serializers
from ..models import *
from student.api.serializers import StudentSerializer
from courses.api.serializers import TeacherSubjectConfigSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    submissions = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()
    assigned_class_details = serializers.SerializerMethodField()
    submissions_count = serializers.SerializerMethodField()
    
    def get_submissions_count(self, obj):
        return len(obj.submission_set.all())
    
    def get_submissions(self, obj):
        return SubmissionSerializer(obj.submission_set.all(), many=True).data
    
    def get_total_count(self, obj):
        a_class = obj.assigned_class
        # course sem shift
        students = Student.objects.filter(
            course = a_class.course,
            shift = a_class.shift,
            semester = a_class.semester
        )
        return len(students)
    
    def get_assigned_class_details(self,obj):
        return TeacherSubjectConfigSerializer(obj.assigned_class).data
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    
    def get_student_name(self, obj):
        return f'{obj.student.user.first_name} {obj.student.user.last_name}'
    
    class Meta:
        model = Submission
        fields = '__all__'