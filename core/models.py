from django.contrib.auth.models import AbstractUser
from django.db import models


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
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    def __str__(self):
        return self.username

class Department(models.Model):  
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.department})'

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    section = models.CharField(max_length=10)
    year = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female')])
    dob = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.roll_number}'

class Faculty(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='faculty_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class FacultyLeave(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=[('Pending','Pending'), ('Approved','Approved'), ('Rejected','Rejected')], default='Pending')

    def __str__(self):
        return f'{self.faculty.user.get_full_name()} - {self.date}'
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.name}"
class Section(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class FacultySubjectMapping(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.CharField(max_length=5)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.faculty} - {self.subject.name} - Y{self.year}S{self.section}"

class TimetableEntry(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    year = models.IntegerField()
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
        return f"{self.course.name} - Y{self.year}S{self.section} - ₹{self.total_amount}"

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    mode = models.CharField(max_length=20, choices=[('Online', 'Online'), ('Offline', 'Offline')])

    def __str__(self):
        return f"{self.student.user.get_full_name()} - ₹{self.amount_paid}"

class Exam(models.Model):
    name = models.CharField(max_length=100)  # e.g., Midterm, Final, Semester 1
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    section = models.CharField(max_length=5)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.course.name} Y{self.year}S{self.section}"

class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()

    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100 if self.total_marks > 0 else 0
    
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

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    target_roles = models.CharField(max_length=255)  # Comma-separated roles
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.sender.username} to {self.receiver.username}"

