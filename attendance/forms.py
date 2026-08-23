from django import forms
from .models import Course, Student, AttendanceSession


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "course_code",
            "course_name",
            "teacher",
        ]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "email",
        ]


class AttendanceSessionForm(forms.ModelForm):

    class Meta:
        model = AttendanceSession

        fields = [
            "course",
            "start_time",
            "end_time",
            "is_active",
        ]

        widgets = {

            "course": forms.Select(
                attrs={
                    "class": "form-select",
                    "style": "display:block !important; width:100% !important; min-height:40px !important;"
                }
            ),

            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "style": "display:block !important; width:100% !important; min-height:40px !important;"
                }
            ),

            "end_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "style": "display:block !important; width:100% !important; min-height:40px !important;"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "style": "display:inline-block !important; width:18px !important; height:18px !important;"
                }
            ),
        }