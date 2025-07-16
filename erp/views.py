from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            if user.role.name == 'Student': return redirect('student_dashboard')
            elif user.role.name == 'Faculty': return redirect('faculty_dashboard')
            elif user.role.name == 'Parent': return redirect('parent_dashboard')
            return redirect('home')
        return render(request, 'erp/auth/login.html', {'error': 'Invalid credentials'})
    return render(request, 'erp/auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'erp/notices/list.html', {'notices': notices})

def attendance_view(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'erp/attendance/mark.html', {'form': form})

