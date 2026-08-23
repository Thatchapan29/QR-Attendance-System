from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Login
    path("login/", views.login_view, name="login"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # =========================
    # Course
    # =========================
    path("courses/", views.course_list, name="courses"),
    path("courses/add/", views.add_course, name="add_course"),
    path("courses/edit/<int:id>/", views.edit_course, name="edit_course"),
    path("courses/delete/<int:id>/", views.delete_course, name="delete_course"),

    # =========================
    # Student
    # =========================
    path("students/", views.student_list, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<int:id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:id>/", views.delete_student, name="delete_student"),
    path("students/import/", views.import_students, name="import_students"),

    # =========================
    # Attendance Session
    # =========================
    path(
        "attendance-sessions/",
        views.attendance_session_list,
        name="attendance_sessions",
    ),
    path(
        "attendance-sessions/add/",
        views.add_attendance_session,
        name="add_attendance_session",
    ),
    path(
        "attendance-sessions/edit/<int:id>/",
        views.edit_attendance_session,
        name="edit_attendance_session",
    ),
    path(
        "attendance-sessions/delete/<int:id>/",
        views.delete_attendance_session,
        name="delete_attendance_session",
    ),
    path(
    "attendance-sessions/qr/<int:id>/",
    views.generate_qr,
    name="generate_qr"
),
]