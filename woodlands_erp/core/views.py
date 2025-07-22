from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from core.models import Role
Role.objects.all()
from django.http import HttpResponseForbidden
from core.models import CustomUser as User
from datetime import date
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, CustomUser , Faculty , Subject ,Parent ,HostelIncharge , Hostel
from .forms import StudentForm, UserForm , FacultyForm , FacultyLeave , FacultyLeaveForm , FacultySubjectMappingForm ,TimetableEntryForm , FacultySubjectMapping , TimetableEntry ,FacultyAttendanceForm
from .forms import Attendance, AttendanceForm , AttendanceRecord , AttendanceRecordForm ,FeePayment , FeePaymentForm , FeeStructure , FeeStructureForm ,AttendanceRecordFormSet  ,FacultyAttendance
from .forms import Mark , MarkForm , Exam , ExamForm , Book , BookForm , BookIssue , BookIssueForm , Message , MessageForm , Notice , NoticeForm 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Vehicle, TransportAllocation
from .forms import VehicleForm, TransportAllocationForm 
from .models import Hostel, HostelRoom, HostelAllocation 
from .models import Result , Department
from .forms import HostelForm, HostelRoomForm, HostelAllocationForm 
from django.db.models import Avg, Count, Sum , F, ExpressionWrapper, DecimalField
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import Attendance, Fee, Student, Mark, Notice
from django.contrib import messages 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.template.loader import get_template
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from django.forms import modelformset_factory
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.template.loader import render_to_string


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            print("✅ LOGIN SUCCESS")
            print("👤 Username:", user.username)
            print("🎯 Role:", repr(getattr(user, 'role', None)))

            role = getattr(user, 'role', '').strip().lower()

            if role in ['superadmin', 'hod', 'faculty', 'student', 'parent', 'librarian', 'accountant', 'transport']:
                return redirect(f'/dashboard/{role}/')
            else:
                return HttpResponse(f"⚠️ Role '{role}' is invalid or not set for this user.")
        else:
            print("❌ LOGIN FAILED: Invalid credentials")
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = user.role

            if role == 'student':
                return redirect('student_form', user_id=user.id)
            elif role == 'faculty':
                return redirect('faculty_form', user_id=user.id)
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/create_user.html', {'form': form})




@login_required

def redirect_dashboard(request):
    role = request.user.role
    return redirect(f'/dashboard/{role}/')

def dashboard_superadmin(request):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/superadmin.html')
@login_required
def dashboard_hostel(request):
    if request.user.role != 'hostel':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/hostel.html')
@login_required
def dashboard_hod(request):
    leaves = FacultyLeave.objects.select_related('faculty__user').all()
    notices = Notice.objects.all().order_by('-posted_on')
    if request.user.role != 'hod':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/hod.html',{'leaves': leaves,'notices' : notices ,'faculty_list': faculty_list })

@login_required
def dashboard_faculty(request):
    notices = Notice.objects.all().order_by('-posted_on')
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/faculty.html', {'notices' : notices })


@login_required
def dashboard_faculty(request):
    faculty = Faculty.objects.get(user=request.user)
    subject_mappings = FacultySubjectMapping.objects.filter(faculty=faculty).select_related('subject__course')
    subjects = [mapping.subject for mapping in subject_mappings]
    exams = Exam.objects.all()
    notices = Notice.objects.all().order_by('-posted_on')
    faculty_leaves = FacultyLeave.objects.filter(faculty=faculty)

    return render(request, 'dashboard/faculty.html', {
        'faculty': faculty,
        'subjects': subjects,
        'exams': exams,
        'notices': notices,
        'faculty_leaves': faculty_leaves
    })

@login_required
def dashboard_student(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("Access Denied")

    try:
        student = Student.objects.select_related('user').get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponseNotFound("Student profile not found. Please contact admin.")
    
    notices = Notice.objects.all().order_by('-posted_on')
    timetable = TimetableEntry.objects.filter(
        course=student.course,
        year=student.year
    ).order_by('day', 'start_time')

    return render(request, 'dashboard/student.html', {
        'student': student,
        'notices': notices,
        'timetable': timetable,
    })

from django.views.decorators.csrf import csrf_exempt



#@login_required
#def student_attendance(request):
 #   student = get_object_or_404(Student, user=request.user)
    #total_classes = AttendanceRecord.objects.filter(student=student).count()
  #  present_days = AttendanceRecord.objects.filter(student=student, status="Present").count()
   # attendance_percent = round((present_days / total_classes) * 100, 2) if total_classes > 0 else 0

    #return render(request, 'student/attendance.html', {
     #   'total_classes': total_classes,
      #  'present_days': present_days,
       # 'attendance_percent': attendance_percent,
    #})


from django.db.models import Sum
from .models import FeeStructure, FeePayment, Student

@login_required
def student_fee(request):
    student = get_object_or_404(Student, user=request.user)

    # Get fee structure for student's course & year
    try:
        fee_structure = FeeStructure.objects.get(course=student.course,year=student.year).first()
        total_fee = fee_structure.total_amount
    except FeeStructure.DoesNotExist:
        total_fee = 0
    payments = FeePayment.objects.filter(student=student)
    total_paid = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_due = total_fee - total_paid

    return render(request, 'student/fee.html', {
        'student': student,
        'total_paid': total_paid,
        'total_due': total_due,
        'total_fee': total_fee,
    })


@login_required
def student_marks(request):
    student = get_object_or_404(Student, user=request.user)
    marks = Mark.objects.filter(student=student)

    return render(request, 'student/marks.html', {
        'marks': marks,
    })


@login_required
def student_timetable(request):
    student = get_object_or_404(Student, user=request.user)
    timetable = TimetableEntry.objects.filter(
        year=student.year,
        section=student.section,
        department=student.department).order_by('day', 'start_time')

    return render(request, 'student/timetable.html', {
        'timetable': timetable,
    })

def add_fee_structure(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            fee_structure = form.save()

            # 🔁 Update all matching students
            students = Student.objects.filter(
                department=fee_structure.department,
                year=fee_structure.year
            )
            for student in students:
                student.total_fee = fee_structure.amount
                student.save()

            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm()
    return render(request, 'fee_structure_add.html', {'form': form})


def dashboard_parent(request):
    try:
        parent = Parent.objects.get(user=request.user)
        child = Student.objects.get(parent=parent)

        # Attendance calculation based on 'Present' / 'Absent' status
        records = AttendanceRecord.objects.filter(student=child)
        present_days = records.filter(status="Present").count()
        total_days = records.count()

        attendance = {
            "present_days": present_days,
            "total_days": total_days,
            "percentage": round((present_days / total_days) * 100, 2) if total_days > 0 else 0
        }

        # Fetch marks
        marks = Mark.objects.filter(student=child)

        return render(request, 'dashboard/parent.html', {
            'child': child,
            'attendance': attendance,
            'marks': marks,
        })

    except (Parent.DoesNotExist, Student.DoesNotExist):
        return render(request, 'dashboard/parent.html', {'child': None})


@login_required
def dashboard_librarian(request):
    if request.user.role != 'librarian':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/librarian.html')

@login_required
def dashboard_accountant(request):
    if request.user.role != 'accountant':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/accountant.html')

@login_required
def dashboard_transport(request):
    if request.user.role != 'transport':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/transport.html')




@login_required
def student_list(request):
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(roll_number__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'students/student_list.html', {
        'students': students,
        'query': query
    })

@login_required
def student_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            # Create user first
            user = user_form.save(commit=False)

            # Set password from cleaned_data
            user.set_password(user_form.cleaned_data['password'])

            # ✅ Assign role as student (case-insensitive)
            student_role = Role.objects.filter(name__iexact='student').first()
            if not student_role:
                return HttpResponse("❌ 'student' role not found in DB.", status=500)
            user.role = student_role

            user.save()

            # Link user to student
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            return redirect('student_list')
    else:
        user_form = UserForm()
        student_form = StudentForm()

    return render(request, 'students/student_form.html', {
        'user_form': user_form,
        'student_form': student_form
    })



@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = student.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            return redirect('student_list')
    else:
        user_form = UserForm(instance=user)
        student_form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'user_form': user_form, 'student_form': student_form})

@login_required
def student_delete(request , pk):
    student = get_object_or_404(Student, pk=pk)
    user = student.user
    user.delete()
    return redirect('student_list')
@login_required
def promote_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if student.year < 4:  # Assuming 4 years total
        student.year += 1
    else:
        student.section = chr(ord(student.section) + 1)  # A → B → C
        student.year = 1  # Reset year
    student.save()
    return redirect('student_list')

@login_required
def student_idcard(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/id_card.html', {'student': student})

@login_required
def faculty_list(request):
    faculty = Faculty.objects.all()
    return render(request, 'faculty/faculty_list.html', {'faculty': faculty})

@login_required
def faculty_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        faculty_form = FacultyForm(request.POST, request.FILES)
        if user_form.is_valid() and faculty_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'faculty'
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            faculty = faculty_form.save(commit=False)
            faculty.user = user
            faculty.save()
            return redirect('faculty_list')
    else:
        user_form = UserForm()
        faculty_form = FacultyForm()
    return render(request, 'faculty/faculty_form.html', {'user_form': user_form, 'faculty_form': faculty_form})

@login_required
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    user = faculty.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        faculty_form = FacultyForm(request.POST, request.FILES, instance=faculty)
        if user_form.is_valid() and faculty_form.is_valid():
            user_form.save()
            faculty_form.save()
            return redirect('faculty_list')
    else:
        user_form = UserForm(instance=user)
        faculty_form = FacultyForm(instance=faculty)
    return render(request, 'faculty/faculty_form.html', {'user_form': user_form, 'faculty_form': faculty_form})

@login_required
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    user = faculty.user
    user.delete()
    return redirect('faculty_list')

@login_required
def faculty_leave_apply(request):
    if request.method == "POST":
        form = FacultyLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.faculty = Faculty.objects.get(user=request.user)  # ✅ important link
            leave.save()
            messages.success(request, "Leave request submitted.")
            return redirect('dashboard_faculty')
    else:
        form = FacultyLeaveForm()
    return render(request, 'faculty/leave_form.html', {'form': form})


@login_required
def faculty_leave_list(request):
    if request.user.role == 'hod':
        leaves = FacultyLeave.objects.all()
    else:
        faculty = get_object_or_404(Faculty, user=request.user)
        leaves = FacultyLeave.objects.filter(faculty=faculty)
    return render(request, 'faculty/leave_list.html', {'leaves': leaves})

def leave_approve(request, pk):
    leave = get_object_or_404(FacultyLeave, pk=pk)
    leave.status = "Approved"
    leave.save()

    faculty = leave.faculty
    subject = "Leave Approved ✅"
    message = f"Hello {faculty.user.get_full_name()},\n\nYour leave on {leave.date} for \"{leave.reason}\" has been approved.\n\nRegards,\nHOD"
    recipient_email = faculty.user.email
    if recipient_email:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )

    messages.success(request, "Leave approved and email sent.")
    return redirect('hod_dashboard')


def leave_reject(request, pk):
    leave = get_object_or_404(FacultyLeave, pk=pk)
    leave.status = "Rejected"
    leave.save()

    faculty = leave.faculty
    subject = "Leave Rejected ❌"
    message = f"Hello {faculty.user.get_full_name()},\n\nYour leave on {leave.date} for \"{leave.reason}\" has been rejected.\n\nRegards,\nHOD"
    recipient_email = faculty.user.email

    if recipient_email:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )

    messages.warning(request, "Leave rejected and email sent.")
    return redirect('hod_dashboard')

@login_required
def subject_mapping_list(request):
    mappings = FacultySubjectMapping.objects.all()
    return render(request, 'faculty/mapping_list.html', {'mappings': mappings})

@login_required
def subject_mapping_add(request):
    if request.method == 'POST':
        form = FacultySubjectMappingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_mapping_list')
    else:
        form = FacultySubjectMappingForm()
    return render(request, 'faculty/mapping_form.html', {'form': form})

@login_required
def timetable_list(request):
    entries = TimetableEntry.objects.all().order_by('day', 'start_time')
    return render(request, 'timetable/timetable_list.html', {'entries': entries})

@login_required
def timetable_add(request):
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_list')
    else:
        form = TimetableEntryForm()
    return render(request, 'timetable/timetable_form.html', {'form': form})

@login_required
def faculty_timetable_view(request):
    faculty = get_object_or_404(Faculty, user=request.user)
    entries = TimetableEntry.objects.filter(faculty=faculty).order_by('day', 'star_time')
    return render(request, 'timetable/faculty_timetable.html', {'entries': entries})


@login_required
def fee_structure_list(request):
    structures = FeeStructure.objects.all()
    return render(request, 'fee/structure_list.html', {'structures': structures})

@login_required
def fee_structure_add(request):
    form = FeeStructureForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('fee_structure_list')
    return render(request, 'fee/structure_form.html', {'form': form})

@login_required
def fee_structure_edit(request, pk):
    structure = get_object_or_404(FeeStructure, pk=pk)
    form = FeeStructureForm(request.POST or None, instance=structure)
    if form.is_valid():
        form.save()
        return redirect('fee_structure_list')
    return render(request, 'fee/structure_form.html', {'form': form})

@login_required
def fee_structure_delete(request, pk):
    structure = get_object_or_404(FeeStructure, pk=pk)
    structure.delete()
    return redirect('fee_structure_list')

@login_required
def fee_payment_list(request):
    payments = FeePayment.objects.all()
    return render(request, 'fee/payment_list.html', {'payments': payments})

@login_required
def fee_payment_add(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            fee_payment = form.save(commit=False)
            fee_payment.total_amount = fee_payment.fee_structure.total_amount  
            fee_payment.save()
            return redirect('fee_payment_list')
    else:
        form = FeePaymentForm()
    return render(request, 'fee/payment_form.html', {'form': form})

@login_required
def generate_fee_receipt_pdf(request, payment_id):
    payment = get_object_or_404(FeePayment, pk=payment_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=receipt_{payment.student.user.username}.pdf'

    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=40)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', parent=styles['Title'], alignment=TA_CENTER, fontSize=18, spaceAfter=20)

    # Title
    elements.append(Paragraph("Fee Payment Receipt", title_style))
    elements.append(Spacer(1, 12))

    # Receipt Info Table
    data = [
        ['Student Name:', payment.student.user.get_full_name()],
        ['Student ID:', payment.student.user.username],
        ['Course:', payment.fee_structure.course.name],
        ['Year:', payment.fee_structure.year],
        ['Total Fee:', f"Rs. {payment.total_amount}"],
        ['Amount Paid:', f"Rs. {payment.amount_paid}"],
        ['Payment Mode:', payment.mode],
        ['Date Paid:', payment.date_paid.strftime('%d-%m-%Y')],
    ]

    table = Table(data, colWidths=[120, 300])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.1, colors.grey),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 40))

    # Footer
    footer = Paragraph("This is a system-generated receipt. No signature required.", styles['Normal'])
    elements.append(footer)

    doc.build(elements)
    return response


@login_required
def exam_list(request):
    exams = Exam.objects.all().order_by('-date')
    return render(request, 'exam/exam_list.html', {'exams': exams})

@login_required
def exam_add(request):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('exam_list')
    Exam.objects.order_by('date')

    return render(request, 'exam/exam_form.html', {'form': form})

@login_required
def mark_entry(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.filter(year=exam.year)
    subjects = Subject.objects.filter(course=exam.subject.course)

    if request.method == 'POST':
        for student in students:
            for subject in subjects:
                mark_key = f'mark_{student.id}_{subject.id}'
                total_key = f'total_{student.id}_{subject.id}'
                marks_obtained = request.POST.get(mark_key)
                total_marks = request.POST.get(total_key)

                if marks_obtained and total_marks:
                    Mark.objects.update_or_create(
                        exam=exam,
                        student=student,
                        subject=subject,
                        defaults={
                            'marks_obtained': marks_obtained,
                            'total_marks': total_marks,
                        }
                    )
        return redirect('exam_list')

    return render(request, 'exam/mark_entry.html', {
        'exam': exam, 'students': students, 'subjects': subjects
    })

@login_required
def view_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    exams = Exam.objects.filter(course=student.course, year=student.year)
    data = []

    for exam in exams:
        marks = Mark.objects.filter(exam=exam, student=student)
        total = sum(m.total_marks for m in marks)
        obtained = sum(m.marks_obtained for m in marks)
        percentage = (obtained / total * 100) if total > 0 else 0
        data.append({'exam': exam, 'marks': marks, 'percentage': round(percentage, 2)})

    return render(request, 'exam/view_result.html', {
        'student': student, 'data': data
    })

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def book_add(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form})

@login_required
def issue_list(request):
    issues = BookIssue.objects.all()
    return render(request, 'library/issue_list.html', {'issues': issues})

@login_required
def issue_book(request):
    form = BookIssueForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('issue_list')
    return render(request, 'library/issue_form.html', {'form': form})

@login_required
def return_book(request, pk):
    issue = get_object_or_404(BookIssue, pk=pk)
    from datetime import date
    issue.returned_on = date.today()
    issue.save()
    return redirect('issue_list')

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'transport/vehicle_list.html', {'vehicles': vehicles})

@login_required
def vehicle_add(request):
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vehicle_list')
    return render(request, 'transport/vehicle_form.html', {'form': form})

@login_required
def assign_transport(request):
    form = TransportAllocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vehicle_list')
    return render(request, 'transport/assign_form.html', {'form': form})

@login_required
def hostel_list(request):
    hostels = Hostel.objects.all()
    return render(request, 'hostel/hostel_list.html', {'hostels': hostels})

@login_required
def hostel_add(request):
    form = HostelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hostel_list')
    return render(request, 'hostel/hostel_form.html', {'form': form})

@login_required
def room_list(request):
    rooms = HostelRoom.objects.all()
    return render(request, 'hostel/room_list.html', {'rooms': rooms})

@login_required
def room_add(request):
    form = HostelRoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hostel_room_list')
    return render(request, 'hostel/room_form.html', {'form': form})

@login_required
def allocate_hostel(request):
    form = HostelAllocationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            allocation = form.save()
            allocation.room.available_beds -= 1
            allocation.room.save()
            return redirect('hostel_room_list')
        else:
            print("❌ Form is invalid:", form.errors)  

    return render(request, 'hostel/allocate_form.html', {'form': form})


@login_required
def notice_list(request):
    notices = Notice.objects.all().order_by('-posted_on')
    return render(request, 'notice_list.html', {'notices': notices})


@login_required
def create_notice(request):
    form = NoticeForm(request.POST or None)
    if form.is_valid():
        notice = form.save(commit=False)
        notice.posted_by = request.user
        notice.save()
        return redirect('notice_list')
    return render(request, 'notice_form.html', {'form': form})

@login_required
def message_list(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, '/message_list.html', {'messages': messages})

@login_required
def send_message(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.sender = request.user
        msg.save()
        return redirect('message_list')
    return render(request, 'messaging/message_form.html', {'form': form})

from collections import defaultdict

@login_required
def fee_report(request):
    data = Fee.objects.values('student__user__first_name').annotate(
        total_paid=Sum('paid_amount'),
        total_due=Sum('amount') - Sum('paid_amount')
    )

    return render(request, 'fee_report.html', {'data': data})

@login_required
def top_performers(request):
    data = Result.objects.values('student__user__first_name').annotate(
        avg_mark=Avg('marks')
    ).order_by('-avg_mark')[:10]
    return render(request, 'top_performers.html', {'data': data})

@login_required
def export_fee_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fee_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Student', 'Total Paid', 'Total Due'])

    data = Fee.objects.values('student__user__first_name').annotate(
        total_paid=Sum('paid_amount'),
        total_due=ExpressionWrapper(
            Sum('amount') - Sum('paid_amount'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    for row in data:
        writer.writerow([
            row['student__user__first_name'],
            row['total_paid'] or 0,
            row['total_due'] or 0
        ])

    return response

@login_required
def fee_report(request):
    data = Fee.objects.values('student__user__first_name').annotate(
        total_paid=Sum('paid_amount'),
        total_due=Sum('amount') - Sum('paid_amount')
    )

    return render(request, 'fee_report_pdf.html', {'data': data})

@login_required
def fee_structure_edit(request, pk):
    fee_structure = get_object_or_404(FeeStructure, pk=pk)
    if request.method == "POST":
        form = FeeStructureForm(request.POST, instance=fee_structure)
        if form.is_valid():
            form.save()
            return redirect('fee_structure_list')  
    else:
        form = FeeStructureForm(instance=fee_structure)
    return render(request, 'fee/structure_form.html', {'form': form})

@login_required
def fee_structure_delete(request, pk):
    fee_structure = get_object_or_404(FeeStructure, pk=pk)
    fee_structure.delete()
    return redirect('fee_structure_list')

def hostel_checkin(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student_id')  # Safe access
        room_number = request.POST.get('room_number')

        if student_id and room_number:
            student = get_object_or_404(Student, id=student_id)
            HostelAllocation.objects.create(student=student, room_number=room_number)
            return redirect('hostel_home')
        else:
            messages.error(request, "Please fill all fields.")

    return render(request, 'hostel/hostel_form.html', {'students': students})


def hostel_checkout(request, pk):
    assignment = get_object_or_404(HostelAllocation, pk=pk)
    if request.method == 'POST':
        assignment.check_out = timezone.now()
        assignment.is_checked_out = True
        assignment.save()
        return redirect('hostel_home')
    return render(request, 'hostel/allocate_form.html', {'assignment':assignment})


@login_required
def allocation_list(request):
    if request.user.role != "transport":
        return HttpResponseForbidden("Access Denied")
    
    allocations = TransportAllocation.objects.select_related('student__user', 'vehicle')
    return render(request, 'transport/allocation.html', {'allocations': allocations})

# Add a new allocation
def allocation_add(request):
    if request.method == 'POST':
        form = TransportAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Transport allocation added successfully.")
            return redirect('transport_allocation_list')
    else:
        form = TransportAllocationForm()
    return render(request, 'transport/allocation_form.html', {'form': form, 'title': 'Add Transport Allocation'})

# Edit existing allocation
def allocation_edit(request, pk):
    allocation = get_object_or_404(TransportAllocation, pk=pk)
    if request.method == 'POST':
        form = TransportAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            messages.success(request, "Transport allocation updated.")
            return redirect('transport_allocation_list')
    else:
        form = TransportAllocationForm(instance=allocation)
    return render(request, 'transport/allocation_form.html', {'form': form, 'title': 'Edit Transport Allocation'})

# Delete an allocation
def allocation_delete(request, pk):
    allocation = get_object_or_404(TransportAllocation, pk=pk)
    allocation.delete()
    messages.warning(request, "Transport allocation deleted.")
    return redirect('transport_allocation_list')

# Toggle paid status
def allocation_toggle_paid(request, pk):
    allocation = get_object_or_404(TransportAllocation, pk=pk)
    allocation.paid = not allocation.paid
    allocation.save()
    messages.info(request, f"Marked as {'Paid' if allocation.paid else 'Unpaid'}.")
    return redirect('transport_allocation_list')

def timetable_print(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="class_timetable.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Full Class Timetable", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    entries = TimetableEntry.objects.all().order_by('day', 'start_time')

    if not entries:
        elements.append(Paragraph("No timetable entries found.", styles['Normal']))
    else:
        data = [["Day", "Start Time", "End Time", "Subject", "Faculty", "Room", "Course"]]

        for entry in entries:
            data.append([
                entry.day,
                entry.start_time.strftime("%I:%M %p"),
                entry.end_time.strftime("%I:%M %p"),
                entry.subject.name,
                entry.faculty.user.get_full_name(),
                entry.room,
                entry.course.name,
            ])

        table = Table(data, repeatRows=1, colWidths=[60, 80, 80, 120, 130, 60, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#11375B")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ]))

        elements.append(table)

    doc.build(elements)
    return response

@login_required
def student_timetable_pdf(request):
    student = get_object_or_404(Student, user=request.user)
    timetable = TimetableEntry.objects.filter(
        year=student.year,
        department=student.department
    ).order_by('day', 'start_time')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="timetable.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph(f" Timetable for {student.user.get_full_name()}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    if not timetable:
        elements.append(Paragraph("No timetable records available.", styles['Normal']))
    else:
        data = [["Day", "Subject", "Start Time", "End Time", "Faculty", "Room No"]]
        for entry in timetable:
            data.append([
                entry.day,
                entry.subject.name,
                entry.start_time.strftime("%I:%M %p"),
                entry.end_time.strftime("%I:%M %p"),
                entry.faculty.user.get_full_name(),
                entry.room
            ])

        table = Table(data, repeatRows=1, colWidths=[60, 120, 80, 80, 130, 60])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#11375B")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)

    doc.build(elements)
    return response


@login_required
def mark_faculty_attendance(request):
    if request.user.role.lower() not in ['superadmin', 'hod']:
        return HttpResponseForbidden("Only SuperAdmin or HOD can mark attendance.")

    if request.method == 'POST':
        form = FacultyAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            return redirect('faculty_attendance_report')
    else:
        form = FacultyAttendanceForm()

    return render(request, 'attendance/mark_faculty_attendance.html', {'form': form})

@login_required
def faculty_attendance_report(request):
    attendance_data = FacultyAttendance.objects.all().order_by('-date')
    return render(request, 'attendance/faculty_attendance_report.html', {'attendance_data': attendance_data})



from django.shortcuts import render
from .models import Mark



from .models import FeePayment

def fee_report(request):
    # Create the HttpResponse object with PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="fee_report.pdf"'

    # Create the PDF object using ReportLab
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Fee Payment Report")

    # Header
    y = height - 100
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Student")
    p.drawString(200, y, "Amount Paid")
    p.drawString(350, y, "Date")

    # Body
    y -= 25
    p.setFont("Helvetica", 10)
    for payment in FeePayment.objects.all():
        p.drawString(50, y, str(payment.student.user.get_full_name()))
        p.drawString(200, y, str(payment.amount_paid))
        p.drawString(350, y, payment.date_paid.strftime('%d-%m-%Y'))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    return response




@login_required
def mark_attendance(request):
    if request.method == 'POST':
        attendance_form = AttendanceForm(request.POST)
        if attendance_form.is_valid():
            attendance = attendance_form.save(commit=False)
            faculty = get_object_or_404(Faculty, user=request.user)
            attendance.faculty = faculty
            attendance.save()

            students = Student.objects.filter(year=attendance.year, section=attendance.section)
            for student in students:
                status = request.POST.get(f'status_{student.id}', 'Absent')
                AttendanceRecord.objects.create(attendance=attendance, student=student, status=status)

            return redirect('view_attendance')
    else:
        attendance_form = AttendanceForm()

    return render(request, 'attendance/mark_attendance.html', {'attendance_form': attendance_form})


@login_required
def view_attendance(request):
    if request.user.role == 'faculty':
        faculty = get_object_or_404(Faculty, user=request.user)
        records = Attendance.objects.filter(faculty=faculty).order_by('-date')
    else:
        records = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/view_attendance.html', {'records': records})

@login_required
def get_students_by_class(request):
    year = request.GET.get('year')
    section = request.GET.get('section')

    students = Student.objects.filter(year=year, section=section)
    data = [{'id': s.id, 'name': s.user.get_full_name()} for s in students]
    return JsonResponse(data, safe=False)

@login_required
def attendance_report(request):
    report = {}

    students = Student.objects.all()
    for student in students:
        records = AttendanceRecord.objects.filter(student=student)
        total = records.count()
        present = records.filter(status='Present').count()
        percentage = (present / total) * 100 if total > 0 else 0

        report[student] = {
            'total': total,
            'present': present,
            'percentage': round(percentage, 2),
        }

    return render(request, 'attendance/attendance_report.html', {'report': report})

@login_required
def student_attendance_view(request):
    student = Student.objects.get(user=request.user)
    attendance_records = AttendanceRecord.objects.filter(student=student).select_related('attendance').order_by('-attendance__date')

    return render(request, 'student/attendance.html', {
        'attendance_records': attendance_records
    })

def gpa_graph_page_view(request):
    return render(request, "reports/gpa_graph.html")

def gpa_report_view(request):
    student_id = request.GET.get('student')
    subject_results = []
    gpa = 0
    percentage = 0

    # Show only students who have marks
    students = Student.objects.filter().distinct()

    if student_id:
        try:
            student = Student.objects.get(id=student_id)
            subject_results = Mark.objects.filter(student=student)

            valid_results = [result for result in subject_results if result.grade_point is not None and result.credits is not None]
            total_credits = sum(result.credits for result in valid_results)
            total_weighted_score = sum(result.grade_point * result.credits for result in valid_results)

            if total_credits > 0:
                gpa = round(total_weighted_score / total_credits, 2)
                percentage = round((gpa / 10) * 100, 2)

        except Student.DoesNotExist:
            student = None

    context = {
        'students': students,
        'subject_results': subject_results,
        'gpa': gpa,
        'percentage': percentage,
        'selected_student_id': int(student_id) if student_id else None
    }
    return render(request, 'reports/gpa_report.html', context)

def gpa_graph_view(request):
    student_id = request.GET.get('student')
    
    if not student_id:
        return JsonResponse({'error': 'Student ID not provided'}, status=400)

    try:
        student = Student.objects.get(id=student_id)
        marks = Mark.objects.filter(student=student)

        data = []
        for mark in marks:
            data.append({
                'subject': str(mark.subject),
                'grade': mark.grade,
                'marks_obtained': mark.marks_obtained,
                'total_marks': mark.total_marks,
                'grade_point': mark.grade_point,
                'credits': mark.credits,
            })

        return JsonResponse({'data': data})
    
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

def gpa_graph_page_view(request):
    students = Student.objects.all()
    student_id = request.GET.get('student')

    context = {
        'students': students,
        'selected_student_id': int(student_id) if student_id and student_id.isdigit() else None,
    }
    return render(request, "reports/gpa_graph.html", context)

from .models import Revenue

def revenue_report_view(request):
    revenues = Revenue.objects.all()
    return render(request, 'revenue/report_revenue.html', {'revenues': revenues})


def calculate_grade_point(marks_obtained, total_marks):
    p = (marks_obtained / total_marks) * 100
    if p >= 90: return 10, 'O'
    elif p >= 80: return 9, 'A+'
    elif p >= 70: return 8, 'A'
    elif p >= 60: return 7, 'B+'
    elif p >= 50: return 6, 'B'
    elif p >= 40: return 5, 'C'
    else: return 0, 'F'

for m in Mark.objects.all():
    if m.grade_point is None:
        gp, grade = calculate_grade_point(m.marks_obtained, m.total_marks)
        m.grade_point = gp
        m.grade = grade
        m.save()