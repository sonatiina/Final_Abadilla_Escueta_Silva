from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Avg, Sum

from .models import Employee, Payslip
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

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
    

def register(request):

    if request.method == "POST":
        username = request.POST.get('newun')
        password = request.POST.get('newpw')
        confirm_password = request.POST.get('conpw')

        if not username or not password or not confirm_password:
            messages.error(request, 'Please fill in all fields')
            return redirect(('register'))
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        User.objects.create(username = username, password = make_password(password))
        messages.success(request, 'Account created Successfully ! Welcome ' + username)
        return render(request, 'payroll_app/login.html')


    return render(request, 'payroll_app/register.html' )


@login_required(login_url='log_in')
def landing(request):
    employees = Employee.objects.all()
    total_employees= Employee.objects.count()
    avSalary = Employee.objects.aggregate(avg_price=Avg("rate", default = 0))['avg_price']
    overtime = Employee.objects.aggregate(total_overtime=Avg("overtime_pay", default = 0))['total_overtime']

    return render(request, 'payroll_app/landing.html', {'employees': employees, 
                                                        'total_employees': total_employees, 
                                                        'avSalary': avSalary, 
                                                        'overtime' : overtime,
                                                        })  


@login_required(login_url='log_in')
def details(request ,pk):
    employee= get_object_or_404(Employee, pk=pk)
    return render(request, 'payroll_app/details.html' , {'employee': employee,})


@login_required(login_url='log_in')
def payDetails(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'payroll_app/payDetails.html', {'payslip': payslip,
                                                        
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
        
        try:
            float(eallowance), float(erate)
        except ValueError:
            messages.info(request, 'Numbers only please')
            return redirect(add_employee)

        eallowance = float(eallowance) if eallowance else None
        eot = 0 
        
        
        if Employee.objects.filter(id_number=eid).exists():
            messages.info(request, 'That ID already exists')
            return redirect(add_employee)
        
        if len(eid) < 6 or len(eid)> 6:
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
def createSlip(request):
    if request.method == "POST":
        currentName = request.POST.get('empList')
        currentMonth = request.POST.get('months')
        currentYear = request.POST.get('year')
        currentCycle = int(request.POST.get('cycle'))

        if Payslip.objects.filter(id_number=currentName, month=currentMonth, year=currentYear, pay_cycle=currentCycle).exists():
            messages.error(request, 'That payslip has already been issued')
            return redirect('payslips')

        if currentName and currentMonth and currentYear and currentCycle:
            try:

                
                employee = Employee.objects.get(pk=currentName)
                allowance = employee.allowance
                base = employee.rate / 2
                ot = employee.overtime_pay * 1.5 * (employee.rate/160)

                pagibig = 0
                ss = 0
                health = 0
                tax = 0
                date = ''
                month = currentMonth
                year = currentYear 
                if currentCycle == 1:
                    pagibig = 100
                    gross = (base + allowance + ot - pagibig) 
                    tax = gross *.2
                    date = f" {month} 1-15, {year}"
                elif currentCycle == 2:
                    
                    health = 0.04 * base
                    ss = 0.045 * base
                    gross = (base + allowance + ot - health - ss) 
                    tax =  gross * .2
                    date = f" {month} 16-30, {year}"
                
                total = gross - tax


                Payslip.objects.create(
                    id_number = employee,
                    month = currentMonth,
                    year = currentYear,
                    pay_cycle = currentCycle,
                    monthlyRate = employee.rate,
                    rate = base,
                    earnings_allowance = employee.allowance,
                    total_pay= total,
                    pag_ibig = pagibig,
                    deductions_health = health,
                    deductions_tax = tax,
                    sss = ss, 
                    overtime = ot,
                    date_range = date
                )

                employee.overtime_pay = 0
                employee.save()

                return redirect('payslips')

            except Employee.DoesNotExist:
                 messages.error(request, "Employee not found.")
        else:
             messages.error(request, "Please fill in all fields")
                
    return render(request, 'payroll_app/payslips.html')

@login_required(login_url='log_in')
def confirm_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'payroll_app/confirm_delete.html' , {'employee': employee,})

@login_required(login_url='log_in')
def remove_employee(request ,pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()

    return redirect('landing')


    

@login_required(login_url='log_in')
def add_overtime(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        addOT = request.POST.get('addot')
        action = request.POST.get('action')

        try:
            addedOT = float(addOT)
        except ValueError:  
            messages.error(request, "Invalid input for overtime hours.")
            return redirect('landing')

        if not addedOT:
            return redirect('landing')
        
        if employee.overtime_pay is None:
            employee.overtime_pay = 0   

        newOvertime = employee.overtime_pay + addedOT

        if newOvertime < 0:
            employee.overtime_pay = 0
            messages.info(request, 'Overtime hours cannot be negative.')

        if newOvertime > 20:
            employee.overtime_pay += 0
            messages.info(request, 'It is illegal to have more than 20 hours ofovertime.')


        else:
            employee.overtime_pay = newOvertime
            if float(addedOT) >= 0:
                messages.info(request, f'{addedOT} overtime hours added!', extra_tags=str(employee.pk)) 
            else:
                messages.info(request, f'{abs(addedOT)} overtime hours deducted!', extra_tags=str(employee.pk))

        employee.save()
        return redirect('landing')

    return render(request, 'payroll_app/landing.html')

@login_required(login_url='log_in')
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        newID = request.POST.get('editID')
        newName = request.POST.get('editName')
        newRate = request.POST.get('editRate')
        newAllowance = request.POST.get('editAllowance')
        newOvertime = request.POST.get('editOt')


        if newID:
            if len(newID) == 6 and newID.isdigit():
                employee.id_number = newID
                messages.success(request, 'ID number changed successfully !')
            elif len(newID) > 6 or len(newID) < 6:
                messages.info(request, 'ID number can only be 6 digits.')
                return redirect('details', pk=employee.pk)
            elif any(char.isalpha() for char in newID):
                messages.info(request, 'ID number cannot have any letters')
                return redirect('details', pk=employee.pk)

            
                                 
        if newName:
            list(newName)
            for letter in newName:
                if letter.isdigit():
                    messages.error(request, 'No numbers in name please!')
                    return redirect ('details', pk=employee.pk)
            else:
                employee.name = newName
            messages.success(request, 'Name changed successfully !')
       
        if newRate:
            if newRate.isdigit():
                employee.rate = newRate
                messages.success(request, 'Allowance successfully adjusted !')
            elif any(char.isalpha() for char in newRate):
                messages.info(request, 'Rate cannot have any letters')
                return redirect('details', pk=employee.pk)
            else:
                messages.info(request, 'Please provide a valid amount.')
                return redirect('details', pk=employee.pk)

            

        if newAllowance:
            if len(newAllowance) and newAllowance.isdigit():
                employee.allowance = newAllowance
                messages.success(request, 'Allowance successfully adjusted !')
            elif any(char.isalpha() for char in newAllowance):
                messages.info(request, 'Allowance cannot have any letters')
                return redirect('details', pk=employee.pk)
            else:
                messages.info(request, 'Please provide a valid amount.')
                return redirect('details', pk=employee.pk)

        if newOvertime:
            if  newOvertime.isdigit():
                employee.overtime_pay = newOvertime
                messages.success(request, 'Overtime Hours successfully adjusted !')
            elif any(char.isalpha() for char in newOvertime):
                messages.info(request, 'Overtime Hours cannot have any letters')
                return redirect('details', pk=employee.pk)
            else:
                messages.info(request, 'Please provide a valid amount.')
                return redirect('details', pk=employee.pk)

        employee.save()

    return render(request, 'payroll_app/details.html', {'employee': employee})

@login_required(login_url='log_in')
def payslips(request):
    employees = Employee.objects.all()
    payslips = Payslip.objects.all()
    return render(request, 'payroll_app/payslips.html', {'employees': employees,
                                                         'payslips': payslips})


def delete_page(request,pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'payroll_app/delete_page.html', {'payslip':payslip,
                                                       })


def delete_slip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    payslip.delete()
    return redirect('payslips')
    
            