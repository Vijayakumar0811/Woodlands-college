from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .models import Student, CustomUser
from .models import Faculty
from .models import FacultyLeave
from .models import FacultySubjectMapping
from .models import TimetableEntry,StudentDocument
from .models import Attendance, AttendanceRecord , FacultyAttendance
from django.forms import modelformset_factory
from .models import FeeStructure, FeePayment
from .models import Exam, Mark
from .models import Book, BookIssue
from .models import Vehicle, TransportAllocation, Hostel, HostelRoom, HostelAllocation
from .models import CourseMaterial
from .models import Notice, Message , Department
from django.contrib.auth import get_user_model
User = get_user_model()
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['register_no', 'department', 'year','section', 'phone' ,'profile_pic']

class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['file']
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        exclude = ['user']


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['department', 'designation', 'phone','subjects' ,'profile_pic']
        

class FacultyLeaveForm(forms.ModelForm):
    class Meta:
        model = FacultyLeave
        fields = ['date', 'reason']


class FacultySubjectMappingForm(forms.ModelForm):
    class Meta:
        model = FacultySubjectMapping
        fields = ['faculty', 'subject', 'year', 'section']

class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        faculty = cleaned_data.get('faculty')
        room = cleaned_data.get('room')
        day = cleaned_data.get('day')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if not all([faculty, room, day, start_time, end_time]):
            return

        # Conflict with same faculty
        faculty_conflict = TimetableEntry.objects.filter(
            faculty=faculty,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if self.instance.pk:
            faculty_conflict = faculty_conflict.exclude(pk=self.instance.pk)

        if faculty_conflict.exists():
            raise forms.ValidationError("⚠️ Faculty is already assigned at this time.")

        # Conflict with same room
        room_conflict = TimetableEntry.objects.filter(
            room=room,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if self.instance.pk:
            room_conflict = room_conflict.exclude(pk=self.instance.pk)

        if room_conflict.exists():
            raise forms.ValidationError("⚠️ Room is already booked at this time.")


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['subject', 'date', 'year', 'section']


class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'status']

AttendanceRecordFormSet = modelformset_factory(
    AttendanceRecord, form=AttendanceRecordForm, extra=0
)



class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_structure', 'amount_paid', 'mode']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'marks_obtained', 'total_marks']



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ['book', 'issued_to', 'return_date']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

class TransportAllocationForm(forms.ModelForm):
    class Meta:
        model = TransportAllocation
        fields = '__all__'

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = '__all__'

class HostelRoomForm(forms.ModelForm):
    class Meta:
        model = HostelRoom
        fields = '__all__'

class HostelAllocationForm(forms.ModelForm):
    class Meta:
        model = HostelAllocation
        fields = '__all__'


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'target_roles']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']

class FacultyAttendanceForm(forms.ModelForm):
    class Meta:
        model = FacultyAttendance
        fields = ['faculty', 'status']

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'course', 'file']