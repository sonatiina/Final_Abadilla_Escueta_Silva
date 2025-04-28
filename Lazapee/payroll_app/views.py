from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Avg, Sum

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
    total_employees= Employee.objects.count()
    avSalary = Employee.objects.aggregate(avg_price=Avg("rate", default = 0))['avg_price']
    overtime = Employee.objects.aggregate(total_overtime=Sum("overtime_pay", default = 0))['total_overtime']

    return render(request, 'payroll_app/landing.html', {'employees': employees, 
                                                        'total_employees': total_employees, 
                                                        'avSalary': avSalary, 
                                                        'overtime' : overtime,
                                                        })  



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
        
        if Employee.objects.filter(id_number=eid).exists():
            messages.info(request, 'That ID already exists')
            return redirect(add_employee)
        
        elif len(eid) < 6 or len(eid)> 6:
            messages.info(request, 'Six digit ID number only')
            return redirect(add_employee)
        
        
        

        elif eid and ename and erate:
           
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

@login_required(login_url='log_in')
def add_overtime(request,pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        addedOT = request.POST.get('addot')
        addedOt_value = int(addedOT) if addedOT else None
        action = request.POST.get('action')

        if addedOt_value is not None:
            if employee.overtime_pay is None:
                employee.overtime_pay = 0

            if action == 'Add Overtime':
                employee.overtime_pay += addedOt_value
                messages.info(request, str(addedOt_value) + ' Overtime hours added!', extra_tags=str(employee.pk))
                
            elif action == 'Deduct Overtime':
                employee.overtime_pay -= addedOt_value
                if employee.overtime_pay < 0:
                    employee.overtime_pay = 0
                    messages.info(request, 'There is no Overtime hours to deduct! ')
                else:
                    messages.info(request, str(addedOt_value) + ' Overtime hours deducted!' , extra_tags=str(employee.pk))
               
            employee.save()
            return redirect('landing')
        else:
            messages.info(request, 'Please fill out the necessary fields.')
            return redirect('landing')

    return render(request, 'payroll_app/landing.html')

