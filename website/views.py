from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record


def home(request):
    active_records = Record.objects.filter(status = True).all()
    inactive_records = Record.objects.filter(status = False).all()
    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In!")
            return redirect('home')

        else:
            messages.success(
                request, "There Was An Error Logging  In, Please Try Again ...")
            return redirect('home')

    else:
        return render(request, 'home.html', {'active_records': active_records, 'inactive_records':inactive_records})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authanticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request,user)
            messages.success(request,"U have successfullt registered! Welcome!!")
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # look for records
        customer_record = Record.objects.get(id=pk)
        
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(
                request, "U must be loggied in to view that page...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(
                    request, "Record Deleted Successfully")
        return redirect('home')
    else:
        messages.success(
                request, "U must be loggied in to do that...")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully!!!")
                return redirect("home")

        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(
                request, "U must be loggied in...")
        return redirect('home')
    

def update_record(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        current_record = Record.objects.get(id = pk)
        form = AddRecordForm(request.GET or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Record has been updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form , 'pk':pk})
    else:
        messages.success(
                request, "U must be loggied in...")
        return redirect('home')


def update_status(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        current_record = Record.objects.get(id = pk)
        current_record.status = not current_record.status
        current_record.save()
        messages.success(request, "status has been updated!")
        return redirect('home')
    else:
        messages.success(
                request, "U must be loggied in...")
        return redirect('home')
    