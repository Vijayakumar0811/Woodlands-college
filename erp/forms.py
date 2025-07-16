class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'period', 'status']
from django import forms
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'admission_no', 'dob', 'class_section']
