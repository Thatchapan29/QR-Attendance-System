from django.urls import path

from .views import (
    attendance_create,
    attendance_session_detail,
    attendance_check,
    attendance_report,
)

urlpatterns = [
    path(
        'create/',
        attendance_create,
        name='attendance_create'
    ),

    path(
        'session/<int:session_id>/',
        attendance_session_detail,
        name='attendance_session_detail'
    ),

    path(
        'check/<str:qr_token>/',
        attendance_check,
        name='attendance_check'
    ),

    path(
        'report/<int:session_id>/',
        attendance_report,
        name='attendance_report'
    ),
]