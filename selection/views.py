from django.shortcuts import render, redirect
from .forms import UserForm, RegistrationForm, LoginForm, SelectionForm, DuesForm, NoDuesForm
from django.http import HttpResponse, Http404
from selection.models import Student, Room, Hostel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')


import logging

# Setup logger
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        # Debugging: Check if form is valid
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            # Create a related Student object
            Student.objects.create(user=new_user)

            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password1'])
            
            # Debugging: Check if user is authenticated and valid
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Debugging: Check the redirection after login
                    logger.info(f"User {cd['username']} logged in successfully.")
                    return redirect('login/edit/')  # Make sure this URL is correct
                else:
                    logger.error("User account is disabled.")
                    return HttpResponse('Disabled account')
            else:
                logger.error(f"Invalid login for {cd['username']}.")
                return HttpResponse('Invalid Login')
        else:
            # If form is invalid, log the errors
            logger.error("Form is invalid")
            logger.error(form.errors)
            return HttpResponse("Form is not valid")
    else:
        form = UserForm()  # Create an empty form for GET requests

    # Always return the render response to show the form
    args = {'form': form}
    return render(request, 'reg_form.html', args)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                if user.is_warden:
                    return HttpResponse('Invalid Login')
                if user.is_active:
                    login(request, user)
                    student = request.user.student
                    return render(request, 'profile.html', {'student': student})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def warden_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                if not user.is_warden:
                    return HttpResponse('Invalid Login')
                elif user.is_active:
                    login(request, user)
                    room_list = request.user.warden.hostel.room_set.all()
                    context = {'rooms': room_list}
                    return render(request, 'warden.html', context)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            student = request.user.student
            return render(request, 'profile.html', {'student': student})
    else:
        form = RegistrationForm(instance=request.user.student)
        return render(request, 'edit.html', {'form': form})


@login_required
def select(request):
    if request.user.student.room:
        room_id_old = request.user.student.room_id

    if request.method == 'POST':
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        
        form = SelectionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                request.user.student.room_allotted = True
                r_id_after = request.user.student.room_id
                room = Room.objects.get(id=r_id_after)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.student.room_allotted = False
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass

            form.save()
            student = request.user.student
            return render(request, 'profile.html', {'student': student})

    else:
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')

        form = SelectionForm(instance=request.user.student)
        student_gender = request.user.student.gender

        # Filter hostels only by gender
        hostels = Hostel.objects.filter(gender=student_gender)
        available_rooms = Room.objects.none()

        # Get all vacant rooms from the filtered hostels
        for hostel in hostels:
            rooms = Room.objects.filter(hostel=hostel, vacant=True)
            available_rooms = available_rooms | rooms  # Combine all vacant rooms
        
        form.fields["room"].queryset = available_rooms  # Set available rooms in the form

        return render(request, 'select_room.html', {'form': form})



@login_required
def warden_dues(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            students = Student.objects.all()
            return render(request, 'dues.html', {'students': students})
    else:
        return HttpResponse('Invalid Login')


@login_required
def warden_add_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = DuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = False
                    student.save()
                    return HttpResponse('Done')
            else:
                form = DuesForm()
                return render(request, 'add_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


@login_required
def warden_remove_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = NoDuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = True
                    student.save()
                    return HttpResponse('Done')
            else:
                form = NoDuesForm()
                return render(request, 'remove_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


def logout_view(request):
    logout(request)
    return redirect('/')





def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {
        'hostel': this_hostel,
        'rooms': Room.objects.filter(
            hostel=this_hostel)}
    return render(request, 'hostels.html', context)

# views.py

from django.shortcuts import render, redirect
from .models import Complaint
from .forms import ComplaintForm

def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            new_complaint = form.save(commit=False)
            new_complaint.student = request.user  # Assign the logged-in student as the user
            new_complaint.save()
            return redirect('complaint_success')  # Redirect to a success page or home page
    else:
        form = ComplaintForm()
    return render(request, 'file_complaint.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Visitor
from .forms import VisitorForm
from django.http import HttpResponse
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student  # Ensure correct import
from .forms import VisitorForm  # Ensure you have this form

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Visitor  # Ensure correct import
from .forms import VisitorForm  # Ensure you have this form

def log_visitor(request):
    if not request.user.is_warden:
        return HttpResponse('Unauthorized', status=403)  # Restrict access

    students = Student.objects.all()  # Fetch students for dropdown
    form = VisitorForm(request.POST or None)  

    if request.method == 'POST':
        if form.is_valid():
            visitor = form.save(commit=False)

            # Get student ID from form data
            student_id = request.POST.get('student')
            try:
                student = Student.objects.get(id=student_id)  # Fetch Student instance
                visitor.student = student.user  # Assign the related User instance
            except Student.DoesNotExist:
                return HttpResponse("Invalid student selected", status=400)  # Handle invalid student

            visitor.warden = request.user  # Assign warden
            visitor.save()
            return redirect('log_visitor')  # Redirect after success

        else:
            print("Form Errors:", form.errors)  # Debugging form errors

    return render(request, 'log_visitor.html', {'form': form, 'students': students})


# views.py
from django.shortcuts import render
from .models import Complaint  # Assuming you have a Complaint model
from .models import Attendance

from django.http import JsonResponse

def view_complaints(request):
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        new_status = request.POST.get("status")

        try:
            complaint = Complaint.objects.get(id=complaint_id)
            if new_status.lower() == "resolved":
                complaint.delete()  # Delete complaint if resolved
                return JsonResponse({"success": True, "deleted": True, "message": "Complaint resolved and deleted."})

            complaint.status = new_status
            complaint.save()
            return JsonResponse({"success": True, "deleted": False, "message": "Status updated successfully."})
        
        except Complaint.DoesNotExist:
            return JsonResponse({"success": False, "message": "Complaint not found."})

    complaints = Complaint.objects.all()
    return render(request, "view_complaints.html", {"complaints": complaints})

@login_required
def view_attendance(request):
    attendance_records = Attendance.objects.filter(student=request.user).order_by('-date')
    return render(request, 'view_attendance.html', {'attendance_records': attendance_records})

from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Student, Attendance  # Ensure correct imports
from django.utils import timezone  # To get the current date and time

def mark_attendance(request):
    if request.method == "POST":
        students = Student.objects.all()
        date_today = timezone.now().date()  # Get today's date
        
        for student in students:
            status = request.POST.get(f"attendance_{student.id}")  # Get attendance status
            if status:
                # Use student.user to assign the User instance
                Attendance.objects.create(student=student.user, status=status, date=date_today)

        messages.success(request, "Attendance marked successfully!")
        return redirect("mark_attendance")  # Redirect to Warden Dashboard after submission
    
    students = Student.objects.all()
    return render(request, "mark_attendance.html", {"students": students})



def visitor_success(request):
    return render(request, 'visitor_success.html')  # Create this template

from django.urls import reverse


def complaint_success(request):
    return redirect(request.META.get('HTTP_REFERER'))