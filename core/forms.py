from django import forms
from .models import Student, CustomUser
from .models import Faculty
from .models import FacultyLeave
from .models import FacultySubjectMapping
from .models import TimetableEntry
from .models import Attendance, AttendanceRecord
from django.forms import modelformset_factory
from .models import FeeStructure, FeePayment
from .models import Exam, Mark
from .models import Book, BookIssue
from .models import Vehicle, TransportAllocation, Hostel, HostelRoom, HostelAllocation
from .models import Notice, Message

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'role']

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'

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