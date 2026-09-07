from django.urls import path

from .views import (
    course_list,
    course_create,
    course_delete,
    enrollment_list,
    enrollment_create,
    enrollment_delete,
)


urlpatterns = [
    path(
        '',
        course_list,
        name='course_list'
    ),

    path(
        'create/',
        course_create,
        name='course_create'
    ),

    path(
        '<int:course_id>/delete/',
        course_delete,
        name='course_delete'
    ),

    path(
        '<int:course_id>/students/',
        enrollment_list,
        name='enrollment_list'
    ),

    path(
        '<int:course_id>/students/add/',
        enrollment_create,
        name='enrollment_create'
    ),

    path(
        'enrollment/<int:enrollment_id>/delete/',
        enrollment_delete,
        name='enrollment_delete'
    ),
]