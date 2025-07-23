from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Student, Faculty, Attendance, Subject, Exam, Book, Hostel, Notice, 
    FeeStructure, FeePayment, TimetableEntry, Vehicle, TransportAllocation,
    HostelRoom, HostelAllocation, FacultyLeave, FacultySubjectMapping,
    Course, CustomUser, Department , Parent , Librarian
    ,Mark)

from .models import Hostel, HostelRoom, HostelAllocation

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_rooms']

from .models import HostelIncharge

@admin.register(HostelIncharge)
class HostelInchargeAdmin(admin.ModelAdmin):
    list_display = ['user', 'contact_number']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']


from django.contrib import admin
from .models import Revenue

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'year')



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    filter_horizontal = ['subjects'] 

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'register_no', 'department', 'year' ]
    list_filter = ['department', 'year']
    fields = ['user', 'register_no', 'department', 'year',  'profile_pic']  


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ['course', 'year', 'day', 'subject', 'faculty', 'start_time', 'end_time']
    autocomplete_fields = ['course',  'subject', 'faculty']
    search_fields = [
        'course__name',
        'subject__name',
        'faculty__user__username'
    ]

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'department', 'year', 'section', 'date', 'start_time', 'end_time')
    list_filter = ('department', 'year', 'section', 'date')
    search_fields = ('name', 'subject__name', 'department__name', 'year', 'section')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'subject',
        'marks_obtained',
        'total_marks',
        'percentage_display',
        'grade',
        'grade_point',
        'credits',
        'get_weighted_score_display',
    )
    list_filter = ('grade', 'subject', 'credits')
    search_fields = ('student__user__first_name', 'subject__name')
    readonly_fields = ('grade_point',)

    def percentage_display(self, obj):
        return f"{obj.percentage():.2f}%" if obj.total_marks else "N/A"
    percentage_display.short_description = "Percentage"

    def get_weighted_score_display(self, obj):
        return obj.get_weighted_score()
    get_weighted_score_display.short_description = "Weighted Score"


admin.site.register(Attendance)
admin.site.register(Book)
admin.site.register(Notice)
admin.site.register(FeeStructure)
admin.site.register(FeePayment)
admin.site.register(Vehicle)
admin.site.register(TransportAllocation)
admin.site.register(HostelRoom)
admin.site.register(HostelAllocation)
admin.site.register(FacultyLeave)
admin.site.register(FacultySubjectMapping)
admin.site.register(Parent)
admin.site.register(Librarian)
