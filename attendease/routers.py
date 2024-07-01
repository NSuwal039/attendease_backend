from rest_framework.routers import DefaultRouter
from authorization.api.viewsets import CustomUserViewset
from assignment.api.viewsets import *
from attendance.api.viewsets import StudentAttendanceViewset, CustomStudentAttendanceViewSet
from courses.api.viewsets import *
from student.api.viewsets import StudentViewSet,StudentSubjectConfigViewSet
from teacher.api.viewsets import TeacherViewSet
from notice.api.viewsets import NoticeViewSet
router = DefaultRouter()

router.register('users', CustomUserViewset, 'users')
router.register('assignments', AssignmentViewset, 'assignments')
router.register('submissions', SubmissionViewset, 'submissions')
router.register('student-attendance', StudentAttendanceViewset, 'student-attendance')
router.register('custom-student-attendance', CustomStudentAttendanceViewSet, 'custom-student-attendance')
# router.register('faculties', FacultyViewset, 'faculties')
router.register('classes', ClassViewset, 'classes')
router.register('students', StudentViewSet, 'students')
router.register('teachers', TeacherViewSet, 'teachers')
router.register('courses', CourseViewset, 'courses')
router.register('subjects', SubjectViewset, 'subjects')
router.register('teacher-subject', TeacherSubjectConfigViewset, 'teacher-subject')
router.register('selected-subjects', StudentSubjectConfigViewSet, 'selected-subjects')
router.register('notices', NoticeViewSet, 'notices')
