from django.db import models
from accounts.models import User


class Course(models.Model):
    course_code = models.CharField(
        max_length=20,
        verbose_name='รหัสวิชา'
    )

    course_name = models.CharField(
        max_length=200,
        verbose_name='ชื่อวิชา'
    )

    description = models.TextField(
        blank=True,
        verbose_name='รายละเอียด'
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'role': 'TEACHER'},
        verbose_name='อาจารย์ผู้สอน'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Enrollment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='รายวิชา'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'STUDENT'},
        verbose_name='นักศึกษา'
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.course.course_code}"