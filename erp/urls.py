from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('students/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('fees/', views.fee_payment_view, name='fees'),
    path('exams/', views.exam_view, name='exams'), 
    path('notices/', views.notice_list, name='notices'),
]
