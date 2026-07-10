from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('questions/', views.generate_questions, name='generate_questions'),
    path('analytics/', views.ai_analytics, name='ai_analytics'),
    path('assignments/', views.assignments_list, name='assignments'),
    path('assignments/<int:pk>/evaluate/', views.evaluate_assignment, name='evaluate_assignment'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('academic-report/', views.academic_report, name='academic_report'),
    path('parent-communication/', views.parent_communication, name='parent_communication'),
    path('accreditation/', views.accreditation_view, name='accreditation'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/assignments/', views.student_assignments, name='student_assignments'),
    path('student/report/', views.student_report, name='student_report'),
    path('', views.dashboard_view, name='home'),
]
