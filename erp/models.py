from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M','Male'),('F','Female')], blank=True)

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=10)

class FacultySubject(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Faculty'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)

class Timetable(models.Model):
    day = models.CharField(max_length=10)
    period = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Faculty'})

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.IntegerField()
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

class Leave(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, default='Pending')

class FeeStructure(models.Model):
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    total_fee = models.DecimalField(max_digits=8, decimal_places=2)

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    receipt_no = models.CharField(max_length=50)

class Exam(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    grade = models.CharField(max_length=5)

class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    available = models.BooleanField(default=True)

class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)


class Vehicle(models.Model):
    route = models.CharField(max_length=50)
    driver = models.CharField(max_length=100)

class TransportAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

class HostelRoom(models.Model):
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

class HostelAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(HostelRoom, on_delete=models.CASCADE)