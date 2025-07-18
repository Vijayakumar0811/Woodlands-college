from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Student, Faculty, Attendance, Subject, Exam, Book, Hostel, Notice, Message,
    FeeStructure, FeePayment, TimetableEntry, Vehicle, TransportAllocation,
    HostelRoom, HostelAllocation, FacultyLeave, FacultySubjectMapping,
    Course, CustomUser, Department, Section
)

# Register related models properly with search_fields if used in autocomplete

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'course', 'section', 'year')
    search_fields = ('roll_number', 'user__username')
    list_filter = ('course', 'section', 'year')

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ['course', 'section', 'year', 'day', 'subject', 'faculty', 'start_time', 'end_time']
    autocomplete_fields = ['course', 'section', 'subject', 'faculty']
    search_fields = [
        'course__name',
        'section__name',
        'subject__name',
        'faculty__user__username'
    ]

# Register remaining models normally
admin.site.register(Attendance)
admin.site.register(Exam)
admin.site.register(Book)
admin.site.register(Hostel)
admin.site.register(Notice)
admin.site.register(Message)
admin.site.register(FeeStructure)
admin.site.register(FeePayment)
admin.site.register(Vehicle)
admin.site.register(TransportAllocation)
admin.site.register(HostelRoom)
admin.site.register(HostelAllocation)
admin.site.register(FacultyLeave)
admin.site.register(FacultySubjectMapping)
