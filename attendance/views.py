from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import pandas as pd
import uuid

from .models import (
    Course,
    Student,
    AttendanceSession,
)

from .forms import (
    CourseForm,
    StudentForm,
    AttendanceSessionForm,
)


# =========================
# Home
# =========================

def home(request):
    return render(request, "attendance/home.html")


# =========================
# Login
# =========================

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "attendance/login.html",
            {
                "error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
            }
        )

    return render(
        request,
        "attendance/login.html"
    )


# =========================
# Dashboard
# =========================

@login_required
def dashboard(request):

    return render(
        request,
        "attendance/dashboard.html"
    )
    # =========================
# Course
# =========================

@login_required
def course_list(request):

    courses = Course.objects.all()

    return render(
        request,
        "attendance/course_list.html",
        {
            "courses": courses
        }
    )


@login_required
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("courses")

    else:

        form = CourseForm()

    return render(
        request,
        "attendance/course_form.html",
        {
            "form": form,
            "title": "เพิ่มรายวิชา"
        }
    )


@login_required
def edit_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            form.save()

            return redirect("courses")

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "attendance/course_form.html",
        {
            "form": form,
            "title": "แก้ไขรายวิชา"
        }
    )


@login_required
def delete_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    if request.method == "POST":

        course.delete()

        return redirect("courses")

    return render(
        request,
        "attendance/course_delete.html",
        {
            "course": course
        }
    )
    # =========================
# Student
# =========================

@login_required
def student_list(request):

    students = Student.objects.all()

    return render(
        request,
        "attendance/student_list.html",
        {
            "students": students
        }
    )


@login_required
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("students")

    else:

        form = StudentForm()

    return render(
        request,
        "attendance/student_form.html",
        {
            "form": form,
            "title": "เพิ่มนักศึกษา"
        }
    )


@login_required
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            return redirect("students")

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "attendance/student_form.html",
        {
            "form": form,
            "title": "แก้ไขนักศึกษา"
        }
    )


@login_required
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        student.delete()

        return redirect("students")

    return render(
        request,
        "attendance/student_delete.html",
        {
            "student": student
        }
    )
    # =========================
# Import Students
# =========================

@login_required
def import_students(request):

    if request.method == "POST":

        excel_file = request.FILES.get("excel_file")

        if excel_file:

            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():

                Student.objects.create(
                    student_id=row["student_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row["email"],
                )

        return redirect("students")

    return render(
        request,
        "attendance/import_students.html"
    )
    # =========================
# Attendance Session
# =========================

@login_required
def attendance_session_list(request):

    sessions = AttendanceSession.objects.all().order_by("-start_time")

    return render(
        request,
        "attendance/attendance_session_list.html",
        {
            "sessions": sessions
        }
    )


@login_required
def add_attendance_session(request):

    if request.method == "POST":

        form = AttendanceSessionForm(request.POST)

        if form.is_valid():

            session = form.save(commit=False)

            # สร้าง QR Token
            session.qr_token = str(uuid.uuid4())

            session.save()

            return redirect("attendance_sessions")

    else:

        form = AttendanceSessionForm()

    return render(
        request,
        "attendance/attendance_session_form.html",
        {
            "form": form,
            "title": "เปิดรอบเช็กชื่อ"
        }
    )


@login_required
def edit_attendance_session(request, id):

    session = get_object_or_404(
        AttendanceSession,
        id=id
    )

    if request.method == "POST":

        form = AttendanceSessionForm(
            request.POST,
            instance=session
        )

        if form.is_valid():

            form.save()

            return redirect("attendance_sessions")

    else:

        form = AttendanceSessionForm(
            instance=session
        )

    return render(
        request,
        "attendance/attendance_session_form.html",
        {
            "form": form,
            "title": "แก้ไขรอบเช็กชื่อ"
        }
    )


@login_required
def delete_attendance_session(request, id):

    session = get_object_or_404(
        AttendanceSession,
        id=id
    )

    if request.method == "POST":

        session.delete()

        return redirect("attendance_sessions")

    return render(
        request,
        "attendance/attendance_session_delete.html",
        {
            "session": session
        }
    )
    # =========================
# QR Code
# =========================

@login_required
def generate_qr(request, id):

    session = get_object_or_404(
        AttendanceSession,
        id=id
    )

    qr_url = (
        f"http://172.20.10.9:8000"
        f"/attendance/{session.qr_token}/"
    )

    return render(
        request,
        "attendance/qr_code.html",
        {
            "session": session,
            "qr_url": qr_url
        }
    )