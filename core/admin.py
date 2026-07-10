from django.contrib import admin
from .models import Faculty, Student, Attendance, Marks, Assignment, AssignmentSubmission, Notification, ParentCommunication

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'user', 'is_verified')
    list_filter = ('department', 'is_verified')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'batch', 'email')
    list_filter = ('batch',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'marked_by')
    list_filter = ('date', 'status', 'student__batch')

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks_obtained', 'max_marks')
    list_filter = ('subject', 'student__batch')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'max_marks', 'created_by', 'created_at')
    list_filter = ('due_date',)

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'ai_score', 'submitted_at')
    list_filter = ('assignment',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')

@admin.register(ParentCommunication)
class ParentCommunicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'sent_at')
    list_filter = ('sent_at',)

