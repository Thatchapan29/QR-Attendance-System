from django.contrib import admin

from .models import (
    AttendanceSession,
    AttendanceToken,
    AttendanceRecord,
)


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):

    list_display = (
        'course',
        'start_time',
        'end_time',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
        'course',
    )

    search_fields = (
        'course__course_code',
        'course__course_name',
    )


@admin.register(AttendanceToken)
class AttendanceTokenAdmin(admin.ModelAdmin):

    list_display = (
        'session',
        'round_number',
        'otp',
        'qr_token',
        'valid_from',
        'valid_until',
    )

    list_filter = (
        'round_number',
    )

    search_fields = (
        'otp',
        'qr_token',
    )


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'session',
        'round_number',
        'checked_in_at',
    )

    list_filter = (
        'round_number',
        'session',
    )

    search_fields = (
        'student__username',
        'session__course__course_code',
        'session__course__course_name',
    )