from django.shortcuts import render, redirect, get_object_or_404

from .models import Supplier, Product

from .forms import CreateUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url = 'log_in')
def main_page(request):
    
    suppliers = Supplier.objects.all()
    return render(request, 'BottleApp/main.html', {'supp': suppliers})

@login_required(login_url = 'log_in')
def bottle_list(request):
    login_required(login_url = 'log_in')
    products = Product.objects.all()
    return render(request, 'BottleApp/list.html', {'prods' : products})

@login_required(login_url = 'log_in')
def supplier_list(request):
   
    suppliers = Supplier.objects.all()    
    return render(request, 'BottleApp/supplier.html', {'supp': suppliers})        

def log_in(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    else:

        if request.method == "POST":
            un = request.POST.get('username')
            pw = request.POST.get('password')

            
            user = authenticate(request, username=un, password=pw)

            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                messages.info(request, 'invalid username or incorrect password')
            
        context = {}
        return render(request, 'BottleApp/login.html', context)

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    else:

        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid ():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account Created Successfully. Welcome ' + user )
                return redirect('log_in')
            else:
               for field, errors in form.errors.items():
                   for error in errors:
                       
                       messages.error(request, f"{field}: {error}")
        return render(request, 'BottleApp/signup.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('log_in')

def add_supplier(request):
    
    if(request.method=="POST"):
        suppname = request.POST.get('sname')
        suppcity = request.POST.get('scity')
        suppcountry = request.POST.get('scountry')
        suppyear = request.POST.get('syear')
        

        if suppname and suppcity and suppcountry and suppyear:
            Supplier.objects.create(
                name=suppname,
                city=suppcity,
                country=suppcountry,
                year = suppyear
            )
        else:
            messages.info(request, "Please fill out all fields.")
            return redirect('main_page')
        return redirect('supplier_list')  
    else:
        return redirect('main_page')
 
def add_product(request):
    if(request.method=="POST"):
        prodname = request.POST.get('pname')
        prodprice = request.POST.get('pprice')
        prodsize = request.POST.get('psize')
        prodmouth = request.POST.get('pmouth')
        prodcolor = request.POST.get('pcolor')
        prodqty = request.POST.get('pqty')
        prodsupplier_id = request.POST.get('psupplier')
        

        if prodname and prodprice and prodsupplier_id and prodsize and prodmouth and prodcolor and prodqty:
            try: 
                supplier = Supplier.objects.get(id=prodsupplier_id)
                Product.objects.create(
                    name = prodname,
                    price = prodprice,
                    supplier = supplier,
                    size = prodsize,
                    mouthsize = prodmouth,
                    color = prodcolor,
                    quantity = prodqty
                )
                return redirect('bottle_list')
            except Supplier.DoesNotExist:
                pass
            suppliers = Supplier.objects.all()
            return render(request, 'BottleApp/main.html', {'supp': suppliers})
            
    else:
        suppliers = Supplier.objects.all()
        return render(request, 'BottleApp/main.html', {'supp':suppliers})
           

@login_required(login_url='log_in')
def details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'BottleApp/details.html', {'product': product})

@login_required(login_url = 'log_in')
def change_name(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        newName = request.POST.get('newname')
        if newName:
            product.name = newName
            product.save()
            # messages.success(request, f'Product name has been changed to {product.name}')
            return redirect('details', pk=product.pk)

    return render(request, 'BottleApp/change_name.html', {'product': product})

@login_required(login_url='log_in')
def supplier_details(request,pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'BottleApp/supplier_details.html', {'supplier':supplier})

@login_required(login_url='log_in')
def change_sname(request,pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        newSupplierName = request.POST.get('newSname')
        if newSupplierName:
            supplier.name = newSupplierName
            supplier.save()
            # messages.success(request, f'Product name has been changed to {product.name}')
            return redirect('supplier_details', pk=supplier.pk)

    return render(request, 'BottleApp/change_sname.html', {'supplier': supplier})


@login_required(login_url='log_in')
def remove_supplier(request,pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')

    

@login_required(login_url='log_in')
def remove_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('bottle_list')

@login_required(login_url = 'log_in')
def manage_account(request):
    return render(request, 'BottleApp/manage_account.html')

@login_required(login_url = 'log_in')
def delete_account(request, pk):
    user = get_object_or_404(User, pk=pk)

    user.delete()
    messages.success(request, 'Your account has been deleted.')
    return redirect('log_in')


@login_required(login_url = 'log_in')
def change_pw(request):
   
    if request.method == "POST":
        current_pw = request.POST.get("current")
        new_pw = request.POST.get("newpw")
        confirm_pw = request.POST.get("confirmpw")

        user = request.user

        if not user.check_password(current_pw):
            messages.error(request, "❌ Current password is incorrect.")
        elif new_pw != confirm_pw:
            messages.error(request, "❌ New passwords do not match.")
        elif current_pw == new_pw:
            messages.error(request, "❌ New password cannot be the same as the current password.")
        else:
            user.set_password(new_pw)
            user.save()
            update_session_auth_hash(request, user) 
            messages.success(request, "✅ Password successfully changed!")
            return redirect('manage_account')

    return render(request, 'BottleApp/change_pw.html')












    
