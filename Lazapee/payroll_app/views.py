from django.shortcuts import render, redirect, get_object_or_404


from .models import Employee
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Create your views here.


def log_in(request):
    if request.user.is_authenticated:
        return redirect('landing')
    else:
        if request.method == 'POST':
            un = request.POST.get('username')
            pw = request.POST.get('pass')
            user = authenticate(request, username = un, password = pw)
            if user is not None:
                login(request, user)
                return redirect('landing')
            else:
                messages.error(request, 'Invalid credentials. Please try again')
        context = {}
        return render(request, 'payroll_app/login.html' ,context)

@login_required(login_url='log_in')
def landing(request):
    employees = Employee.objects.all()
    return render(request, 'payroll_app/landing.html', {'employees': employees})

@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')


@login_required(login_url='log_in')
def add_employee(request):
    if request.method == 'POST':
        eid = request.POST.get('num')
        ename = request.POST.get('name')
        erate = request.POST.get('rate')
        eallowance = request.POST.get('allowance')
        eot = request.POST.get('overtime')

        eallowance = float(eallowance) if eallowance else None

        if eid and ename and erate:
            Employee.objects.create(
                name = ename,
                id_number = eid,
                rate = erate,
                allowance = eallowance,
                overtime_pay = eot
            )
            messages.info(request, 'Employee Added !')
        
       
        else: 
            messages.info(request, 'Please fill out the necessary fields')
            return redirect('add_employee')
            
        return redirect('landing')

    return render(request, 'payroll_app/add_employee.html')

@login_required(login_url='log_in')
def remove_employee(request ,pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()

    return redirect('landing')