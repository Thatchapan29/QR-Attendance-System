from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    UserLoginView,
    dashboard,
    student_dashboard,
    teacher_dashboard,
    admin_dashboard,
    teacher_attendance_history,
)

urlpatterns = [
    path(
        'login/',
        UserLoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='/login/'),
        name='logout'
    ),

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    path(
        'student/',
        student_dashboard,
        name='student_dashboard'
    ),

    path(
        'teacher/',
        teacher_dashboard,
        name='teacher_dashboard'
    ),

    path(
        'teacher/attendance-history/',
        teacher_attendance_history,
        name='teacher_attendance_history'
    ),

    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),
]