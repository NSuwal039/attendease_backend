from rest_framework.routers import DefaultRouter
from authorization.api.viewsets import CustomUserViewset
from assignment.api.viewsets import *
from attendance.api.viewsets import StudentAttendanceViewset
from courses.api.viewsets import *
from student.api.viewsets import StudentViewSet
from teacher.api.viewsets import TeacherViewSet
router = DefaultRouter()

router.register('users', CustomUserViewset, 'users')
router.register('assignments', AssignmentViewset, 'assignments')
router.register('submissions', SubmissionViewset, 'submissions')
router.register('student-attendance', StudentAttendanceViewset, 'student-attendance')
# router.register('faculties', FacultyViewset, 'faculties')
router.register('classes', ClassViewset, 'classes')
router.register('students', StudentViewSet, 'students')
router.register('teachers', TeacherViewSet, 'teachers')
