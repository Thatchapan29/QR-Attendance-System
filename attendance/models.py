from django.db import models
from django.utils import timezone
from courses.models import Course


class AttendanceSession(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='attendance_sessions',
        verbose_name='รายวิชา'
    )

    start_time = models.DateTimeField(
        verbose_name='เวลาเริ่มเช็คชื่อ'
    )

    end_time = models.DateTimeField(
        verbose_name='เวลาสิ้นสุดเช็คชื่อ'
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name='เปิดเช็คชื่อ'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.course.course_code} - "
            f"{self.start_time.strftime('%d/%m/%Y %H:%M')}"
        )

    def is_open(self):
        now = timezone.now()

        return (
            self.is_active
            and self.start_time <= now <= self.end_time
        )
        import secrets
from django.db import models
from django.utils import timezone


class AttendanceToken(models.Model):

    session = models.ForeignKey(
        'AttendanceSession',
        on_delete=models.CASCADE,
        related_name='tokens',
        verbose_name='การเช็คชื่อ'
    )

    round_number = models.PositiveSmallIntegerField(
        verbose_name='รอบ'
    )

    otp = models.CharField(
        max_length=6,
        verbose_name='OTP'
    )

    qr_token = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='QR Token'
    )

    valid_from = models.DateTimeField(
        verbose_name='เริ่มใช้'
    )

    valid_until = models.DateTimeField(
        verbose_name='หมดอายุ'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_valid(self):

        now = timezone.now()

        return (
            self.valid_from <= now < self.valid_until
            and self.session.is_open()
        )

    def __str__(self):

        return (
            f"{self.session.course.course_code} - "
            f"รอบ {self.round_number} - "
            f"OTP {self.otp}"
        )
class AttendanceRecord(models.Model):

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='การเช็คชื่อ'
    )

    student = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='นักศึกษา'
    )

    token = models.ForeignKey(
        AttendanceToken,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='Token'
    )

    round_number = models.PositiveSmallIntegerField(
        verbose_name='รอบ'
    )

    checked_in_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='เวลาเช็คชื่อ'
    )

    def __str__(self):
        return (
            f"{self.student.username} - "
            f"{self.session.course.course_code} - "
            f"รอบ {self.round_number}"
        )
class AttendanceAttempt(models.Model):

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='attendance_attempts',
        verbose_name='การเช็คชื่อ'
    )

    student = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='attendance_attempts',
        verbose_name='นักศึกษา'
    )

    token = models.ForeignKey(
        AttendanceToken,
        on_delete=models.CASCADE,
        related_name='attendance_attempts',
        verbose_name='Token'
    )

    otp_entered = models.CharField(
        max_length=6,
        verbose_name='OTP ที่กรอก'
    )

    is_correct = models.BooleanField(
        default=False,
        verbose_name='OTP ถูกต้อง'
    )

    attempted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='เวลาที่ส่ง'
    )

    def __str__(self):
        return (
            f"{self.student.username} - "
            f"{self.session.course.course_code} - "
            f"ครั้งที่ {self.id}"
        )