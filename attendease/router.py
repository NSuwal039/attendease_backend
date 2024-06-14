from rest_framework.routers import DefaultRouter
from courses.api.viewsets import *
from student.api.viewsets import *

router = DefaultRouter()

router.register('faculties', FacultyViewset, 'faculties')
router.register('students', StudentViewSet, 'students')