from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from .models import Course, Enrollment


@login_required
def course_list(request):
    if request.user.role == 'TEACHER':
        courses = Course.objects.filter(
            teacher=request.user
        )

    elif request.user.role == 'ADMIN':
        courses = Course.objects.all()

    else:
        return redirect('dashboard')

    return render(
        request,
        'courses/course_list.html',
        {'courses': courses}
    )


@login_required
def course_create(request):
    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        course_name = request.POST.get('course_name')
        description = request.POST.get('description')

        Course.objects.create(
            course_code=course_code,
            course_name=course_name,
            description=description,
            teacher=request.user
        )

        return redirect('course_list')

    return render(
        request,
        'courses/course_form.html'
    )


@login_required
def course_delete(request, course_id):
    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    if request.method == 'POST':
        course.delete()
        return redirect('course_list')

    return render(
        request,
        'courses/course_delete.html',
        {'course': course}
    )


@login_required
def enrollment_list(request, course_id):
    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    enrollments = course.enrollments.select_related(
        'student'
    )

    students = User.objects.filter(
        role='STUDENT'
    ).order_by('username')

    return render(
        request,
        'courses/enrollment_list.html',
        {
            'course': course,
            'enrollments': enrollments,
            'students': students,
        }
    )


@login_required
def enrollment_create(request, course_id):
    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    if request.method == 'POST':
        student_id = request.POST.get('student')

        student = get_object_or_404(
            User,
            id=student_id,
            role='STUDENT'
        )

        Enrollment.objects.get_or_create(
            course=course,
            student=student
        )

    return redirect(
        'enrollment_list',
        course_id=course.id
    )


@login_required
def enrollment_delete(request, enrollment_id):
    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        course__teacher=request.user
    )

    if request.method == 'POST':
        course_id = enrollment.course.id
        enrollment.delete()

        return redirect(
            'enrollment_list',
            course_id=course_id
        )

    return redirect(
        'enrollment_list',
        course_id=enrollment.course.id
    )