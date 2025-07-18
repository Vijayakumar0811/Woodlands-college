from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponseForbidden 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, CustomUser , Faculty , Subject 
from .forms import StudentForm, UserForm , FacultyForm , FacultyLeave , FacultyLeaveForm , FacultySubjectMappingForm ,TimetableEntryForm , FacultySubjectMapping , TimetableEntry 
from .forms import Attendance, AttendanceForm , AttendanceRecord , AttendanceRecordForm ,FeePayment , FeePaymentForm , FeeStructure , FeeStructureForm
from .forms import Mark , MarkForm , Exam , ExamForm , Book , BookForm , BookIssue , BookIssueForm , Message , MessageForm , Notice , NoticeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Vehicle, TransportAllocation
from .forms import VehicleForm, TransportAllocationForm 
from .models import Hostel, HostelRoom, HostelAllocation 
from .forms import HostelForm, HostelRoomForm, HostelAllocationForm 
from django.db.models import Avg, Count, Sum
from django.http import HttpResponse
import csv
from .models import Attendance 
from django.contrib import messages 


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



@login_required

def redirect_dashboard(request):
    role = request.user.role
    return redirect(f'/dashboard/{role}/')

def dashboard_superadmin(request):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/superadmin.html')

@login_required
def dashboard_hod(request):
    if request.user.role != 'hod':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/hod.html')

@login_required
def dashboard_faculty(request):
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/faculty.html')

@login_required
def dashboard_student(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/student.html')

@login_required
def dashboard_parent(request):
    if request.user.role != 'parent':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/parent.html')

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
@login_required
def student_timetable_view(request):
    try:
        student = request.user.student  
    except:
        return HttpResponse("No student profile linked to this user.")

    timetable = TimetableEntry.objects.filter(
        course=student.course,
        section=student.section,
        year=student.year
    )
    return render(request, 'student/timetable.html', {'timetable': timetable})

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
            user = user_form.save(commit=False)
            user.role = 'student'
            user.set_password('woodlands123')  # default password
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('student_list')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    return render(request, 'students/student_form.html', {'user_form': user_form, 'student_form': student_form})

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
            user.set_password('woodlands123')
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
    faculty = get_object_or_404(Faculty, user=request.user)
    if request.method == 'POST':
        form = FacultyLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.faculty = faculty
            leave.save()
            return redirect('faculty_leave_list')
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

@login_required
def leave_approve(request, pk):
    leave = get_object_or_404(FacultyLeave, pk=pk)
    leave.status = 'Approved'
    leave.save()
    return redirect('faculty_leave_list')

@login_required
def leave_reject(request, pk):
    leave = get_object_or_404(FacultyLeave, pk=pk)
    leave.status = 'Rejected'
    leave.save()
    return redirect('faculty_leave_list')

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
    entries = TimetableEntry.objects.all().order_by('day', 'period')
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
    entries = TimetableEntry.objects.filter(faculty=faculty).order_by('day', 'period')
    return render(request, 'timetable/faculty_timetable.html', {'entries': entries})

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
def fee_payment_list(request):
    payments = FeePayment.objects.all()
    return render(request, 'fee/payment_list.html', {'payments': payments})

@login_required
def fee_payment_add(request):
    form = FeePaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('fee_payment_list')
    return render(request, 'fee/payment_form.html', {'form': form})

@login_required
def exam_list(request):
    exams = Exam.objects.all().order_by('-start_date')
    return render(request, 'exam/exam_list.html', {'exams': exams})

@login_required
def exam_add(request):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('exam_list')
    return render(request, 'exam/exam_form.html', {'form': form})

@login_required
def mark_entry(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.filter(year=exam.year, section=exam.section)
    subjects = Subject.objects.filter(course=exam.course)

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
    exams = Exam.objects.filter(course=student.course, year=student.year, section=student.section)
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
        return redirect('room_list')
    return render(request, 'hostel/room_form.html', {'form': form})

@login_required
def allocate_hostel(request):
    form = HostelAllocationForm(request.POST or None)
    if form.is_valid():
        allocation = form.save()
        allocation.room.available_beds -= 1
        allocation.room.save()
        return redirect('room_list')
    return render(request, 'hostel/allocate_form.html', {'form': form})

@login_required
def notice_list(request):
    role = request.user.role.lower()
    notices = Notice.objects.filter(target_roles__icontains=role)
    return render(request, 'noticeboard/notice_list.html', {'notices': notices})

@login_required
def create_notice(request):
    form = NoticeForm(request.POST or None)
    if form.is_valid():
        notice = form.save(commit=False)
        notice.posted_by = request.user
        notice.save()
        return redirect('notice_list')
    return render(request, 'noticeboard/notice_form.html', {'form': form})

@login_required
def message_list(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'messaging/message_list.html', {'messages': messages})

@login_required
def send_message(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.sender = request.user
        msg.save()
        return redirect('message_list')
    return render(request, 'messaging/message_form.html', {'form': form})

@login_required
def attendance_report(request):
    data = Attendance.objects.values('student__user__first_name').annotate(
        total_days=Count('date'),
        days_present=Count('is_present', filter= Q(is_present=True))
    )
    return render(request, 'reports/attendance_report.html', {'data': data})

@login_required
def fee_report(request):
    data = Fee.objects.values('student__user__first_name').annotate(
        total_paid=Sum('paid_amount'),
        total_due=Sum('total_amount') - Sum('paid_amount')
    )
    return render(request, 'reports/fee_report.html', {'data': data})

@login_required
def top_performers(request):
    data = Result.objects.values('student__user__first_name').annotate(
        avg_mark=Avg('marks')
    ).order_by('-avg_mark')[:10]
    return render(request, 'reports/top_performers.html', {'data': data})

@login_required
def export_fee_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fee_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Student', 'Total Paid', 'Total Due'])

    data = Fee.objects.values('student__user__first_name').annotate(
        total_paid=Sum('paid_amount'),
        total_due=Sum('total_amount') - Sum('paid_amount')
    )
    for row in data:
        writer.writerow([row['student__user__first_name'], row['total_paid'], row['total_due']])

    return response