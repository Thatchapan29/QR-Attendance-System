from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from attendance.models import AttendanceSession

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.POST.get('next')

        if next_url:
            return next_url

        return '/dashboard/'


@login_required
def dashboard(request):

    if request.user.role == 'STUDENT':
        return redirect('student_dashboard')

    elif request.user.role == 'TEACHER':
        return redirect('teacher_dashboard')

    elif request.user.role == 'ADMIN':
        return redirect('admin_dashboard')

    return redirect('login')


@login_required
def student_dashboard(request):

    if request.user.role != 'STUDENT':
        return redirect('dashboard')

    return render(
        request,
        'student/dashboard.html'
    )


@login_required
def teacher_dashboard(request):

    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    sessions = AttendanceSession.objects.filter(
        course__teacher=request.user
    ).select_related(
        'course'
    ).order_by(
        '-start_time'
    )

    return render(
        request,
        'teacher/dashboard.html',
        {
            'sessions': sessions,
        }
    )


@login_required
def admin_dashboard(request):

    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    return render(
        request,
        'admin/dashboard.html'
    )
@login_required
def teacher_attendance_history(request):

    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    sessions = AttendanceSession.objects.filter(
        course__teacher=request.user
    ).select_related(
        'course'
    ).order_by(
        '-start_time'
    )

    return render(
        request,
        'teacher/attendance_history.html',
        {
            'sessions': sessions,
        }
    )