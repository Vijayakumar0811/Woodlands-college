from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('hod', 'HOD'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('librarian', 'Librarian'),
        ('accountant', 'Accountant'),
        ('transport', 'Transport Staff'),
        ('hostel','Hostel Incharge')
    
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    def __str__(self):
        return self.username
from django.conf import settings
from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Department(models.Model):  
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} '
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ManyToManyField('Student')


    def __str__(self):
        return f"{self.code} - {self.name}"  



from django.contrib.auth.models import User




def student_photo_path(instance, filename):
    return f"student_photos/{filename}"

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    register_no = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)  
    year = models.IntegerField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="students")
    section = models.CharField(max_length=10)


    

    def __str__(self):
        return f"{self.user.first_name} ({self.register_no})"


class Faculty(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='faculty_photos/', null=True, blank=True)
    subjects = models.ManyToManyField('Subject', blank=True)
    def __str__(self):
        return self.user.get_full_name()
    

class FacultyLeave(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=[('Pending','Pending'), ('Approved','Approved'), ('Rejected','Rejected')], default='Pending')

    def __str__(self):
        return f'{self.faculty.user.get_full_name()} - {self.date}'
    


    
class FacultySubjectMapping(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField()
    section = models.CharField(max_length=5)


    def __str__(self):
        return f"{self.faculty} - {self.subject.name} - Y{self.year}"


class TimetableEntry(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    section = models.CharField(max_length=5)

    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    room = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.day} - {self.subject.name}"
    

class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    year = models.IntegerField()
    section = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.subject.name} - {self.date}"

class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.status}"

class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    section = models.CharField(max_length=5)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.course.name} - Y{self.year} - ₹{self.total_amount}"

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    mode = models.CharField(max_length=20, choices=[('Online', 'Online'), ('Offline', 'Offline')])

    def __str__(self):
        return f"{self.student.user.get_full_name()} - ₹{self.amount_paid}"

class Exam(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.CharField(max_length=10)
    section = models.CharField(max_length=5)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject.name if self.subject else 'N/A'}"



    
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_to = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned_on = models.DateField(null=True, blank=True)

    def is_late(self):
        from datetime import date
        return self.returned_on and self.returned_on > self.return_date

    def fine_amount(self):
        if self.is_late():
            delta = (self.returned_on - self.return_date).days
            return delta * 10  # ₹10/day fine
        return 0

class Vehicle(models.Model):
    number_plate = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100)
    route = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.number_plate} - {self.route}"

class TransportAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.vehicle.number_plate}"

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    total_rooms = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

class HostelIncharge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username()

class HostelRoom(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    available_beds = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class HostelAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(HostelRoom, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)
    hostel_fee = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - Room {self.room.room_number}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.sender.username} to {self.receiver.username}"

class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Due', 'Due'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return f"{self.student} - ₹{self.amount} ({self.status})"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

from django.conf import settings
from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  
        blank=True
    )
    target_roles = models.CharField(max_length=100, default='all')
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"
    
class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Librarian: {self.user.get_full_name()}"

class FacultyAttendance(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    marked_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Superadmin or HOD


GRADE_CHOICES = [
    ('O', 'Outstanding'),
    ('A+', 'Excellent'),
    ('A', 'Very Good'),
    ('B+', 'Good'),
    ('B', 'Average'),
    ('C', 'Pass'),
    ('F', 'Fail'),
]

GRADE_POINTS = {
    'O': 10,
    'A+': 9,
    'A': 8,
    'B+': 7,
    'B': 6,
    'C': 5,
    'F': 0,
}



class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    marks_obtained = models.FloatField()
    credits = models.PositiveIntegerField(default=4)
    grade_point = models.FloatField(null=True, blank=True)
    total_marks = models.FloatField()

    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100 if self.total_marks > 0 else 0

    def get_grade_point(self):
        return GRADE_POINTS.get(self.grade, 0)

    def get_weighted_score(self):
        return self.get_grade_point() * self.credits

    def _str_(self):
        return f"{self.student.name} - {self.subject} ({self.grade})"
    
def save(self, *args, **kwargs):
    self.grade_point = self.calculate_grade_point()
    super().save(*args, **kwargs)

def calculate_grade_point(self):
    # Example logic: you can customize this
    if self.marks >= 90:
        return 10
    elif self.marks >= 80:
        return 9
    elif self.marks >= 70:
        return 8
    elif self.marks >= 60:
        return 7
    elif self.marks >= 50:
        return 6
    else:
        return 0


class Revenue(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    date = models.DateField()
    year = models.IntegerField()
    def _str_(self):
        return f"{self.source} - ₹{self.amount}"