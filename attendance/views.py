import secrets
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from courses.models import Course
from .models import (
    AttendanceSession,
    AttendanceToken,
    AttendanceRecord,
    AttendanceAttempt,
)


def generate_otp():
    return f"{secrets.randbelow(1000000):06d}"


@login_required
def attendance_create(request):

    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    courses = Course.objects.filter(
        teacher=request.user
    )

    if request.method == 'POST':

        course_id = request.POST.get('course')

        course = get_object_or_404(
            Course,
            id=course_id,
            teacher=request.user
        )

        start_time = timezone.now()

        end_time = start_time + timedelta(
            minutes=6
        )

        session = AttendanceSession.objects.create(
            course=course,
            start_time=start_time,
            end_time=end_time,
            is_active=True
        )

        # 3 รอบ × 2 นาที
        # แต่ละรอบมี 4 OTP
        # OTP เปลี่ยนทุก 30 วินาที

        for round_number in range(1, 4):

            round_start = start_time + timedelta(
                minutes=(round_number - 1) * 2
            )

            for slot in range(4):

                token_start = round_start + timedelta(
                    seconds=slot * 30
                )

                token_end = token_start + timedelta(
                    seconds=30
                )

                AttendanceToken.objects.create(
                    session=session,
                    round_number=round_number,
                    otp=generate_otp(),
                    qr_token=secrets.token_urlsafe(32),
                    valid_from=token_start,
                    valid_until=token_end
                )

        return redirect(
            'attendance_session_detail',
            session_id=session.id
        )

    return render(
        request,
        'attendance/attendance_create.html',
        {
            'courses': courses
        }
    )


@login_required
def attendance_session_detail(request, session_id):

    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    session = get_object_or_404(
        AttendanceSession,
        id=session_id,
        course__teacher=request.user
    )

    tokens = session.tokens.order_by(
        'round_number',
        'valid_from'
    )

    return render(
        request,
        'attendance/attendance_session_detail.html',
        {
            'session': session,
            'tokens': tokens,
        }
    )


@login_required
def attendance_check(request, qr_token):

    token = get_object_or_404(
        AttendanceToken,
        qr_token=qr_token
    )

    session = token.session

    # ต้องเป็นนักศึกษาเท่านั้น
    if request.user.role != 'STUDENT':
        return redirect('dashboard')

    # ตรวจสอบว่า QR ยังใช้งานได้
    if not token.is_valid():

        return render(
            request,
            'attendance/attendance_check.html',
            {
                'error': 'QR Code หมดอายุหรือปิดการเช็คชื่อแล้ว'
            }
        )

    # ตรวจสอบว่านักศึกษาลงทะเบียนวิชานี้หรือไม่
    is_enrolled = session.course.enrollments.filter(
        student=request.user
    ).exists()

    if not is_enrolled:

        return render(
            request,
            'attendance/attendance_check.html',
            {
                'error': 'คุณไม่ได้ลงทะเบียนเรียนในรายวิชานี้'
            }
        )

    # ตรวจสอบว่าเช็คชื่อสำเร็จไปแล้วหรือยัง
    already_checked = AttendanceRecord.objects.filter(
        session=session,
        student=request.user
    ).exists()

    if already_checked:

        return render(
            request,
            'attendance/attendance_check.html',
            {
                'success': 'เช็คชื่อสำเร็จ',
                'session': session,
                'token': token,
            }
        )

    # นับจำนวนครั้งที่นักศึกษาส่ง OTP
    attempt_count = AttendanceAttempt.objects.filter(
        session=session,
        student=request.user
    ).count()

    # จำกัดสูงสุด 4 ครั้ง
    if attempt_count >= 4:

        return render(
            request,
            'attendance/attendance_check.html',
            {
                'error': 'คุณส่ง OTP ครบ 4 ครั้งแล้ว',
                'session': session,
                'token': token,
            }
        )

    if request.method == 'POST':

        otp = request.POST.get(
            'otp',
            ''
        ).strip()

        # ตรวจสอบ OTP
        is_correct = otp == token.otp

        # บันทึกประวัติการพยายาม
        AttendanceAttempt.objects.create(
            session=session,
            student=request.user,
            token=token,
            otp_entered=otp,
            is_correct=is_correct
        )

        # OTP ผิด
        if not is_correct:

            remaining_attempts = 3 - attempt_count

            return render(
                request,
                'attendance/attendance_check.html',
                {
                    'error': (
                        'OTP ไม่ถูกต้อง '
                        f'เหลืออีก {remaining_attempts} ครั้ง'
                    ),
                    'session': session,
                    'token': token,
                }
            )

        # OTP ถูกต้อง → บันทึกการเข้าเรียน
        AttendanceRecord.objects.create(
            session=session,
            student=request.user,
            token=token,
            round_number=token.round_number
        )

        return render(
            request,
            'attendance/attendance_check.html',
            {
                'success': 'เช็คชื่อสำเร็จ',
                'session': session,
                'token': token,
            }
        )

    return render(
        request,
        'attendance/attendance_check.html',
        {
            'session': session,
            'token': token,
        }
    )
@login_required
def attendance_report(request, session_id):

    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    session = get_object_or_404(
        AttendanceSession,
        id=session_id,
        course__teacher=request.user
    )

    enrollments = session.course.enrollments.select_related(
        'student'
    )

    records = AttendanceRecord.objects.filter(
        session=session
    ).select_related(
        'student'
    )

    record_map = {
        record.student_id: record
        for record in records
    }

    students = []

    for enrollment in enrollments:

        record = record_map.get(
            enrollment.student_id
        )

        students.append({
            'student': enrollment.student,
            'record': record,
            'checked': record is not None,
        })

    total_students = len(students)

    checked_students = sum(
        1
        for student in students
        if student['checked']
    )

    return render(
        request,
        'attendance/attendance_report.html',
        {
            'session': session,
            'students': students,
            'total_students': total_students,
            'checked_students': checked_students,
        }
    )