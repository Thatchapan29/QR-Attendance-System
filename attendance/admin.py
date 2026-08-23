from django.contrib import admin
from .models import (
    Teacher,
    Student,
    Course,
    Enrollment,
    AttendanceSession,
    Attendance
)

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(AttendanceSession)
admin.site.register(Attendance)