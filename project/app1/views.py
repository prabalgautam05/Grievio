from django.shortcuts import render, HttpResponse, redirect
from .models import Complaint, Department, Assign
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, aauthenticate, get_backends
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, get_object_or_404
 


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Allotted', 'Allotted'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Rejected', 'Rejected')
)




def submit_complaint(request):
    departments = Department.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        department_id = request.POST.get('department')
        raised_by = request.POST.get('raised_by')
        resolution_time = request.POST.get('resolution_time')
        email = request.POST.get('Email')
        phone_number = request.POST.get('Phone_number')
        
        # Handle image upload
        image = request.FILES.get('image')

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            department = None

        # Validate phone number length
        if len(phone_number) != 10 or not phone_number.isdigit():
            return render(request, 'complaint_form.html', {
                'departments': departments,
                'error': 'Phone number must be exactly 10 digits.'
            })

        # Prepend +91 to the phone number
        phone_number = '+91' + phone_number

        # Create the Complaint object without complaint_date
        complaint = Complaint.objects.create(
            title=title,    
            description=description,
            department=department,
            raised_by=raised_by,
            resolution_time=resolution_time,
            image=image,
            Email=email,
            Phone_number=phone_number,
        )

        # Redirect to a success page to prevent duplicate form submissions on refresh
        return redirect('complaint_success', complaint_id=complaint.id)
    
    return render(request, 'complaint_form.html', {'departments': departments})

def complaint_success(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    return HttpResponse(f"Complaint submitted successfully. Complaint number is: {complaint.id}")

def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    context = {
        'complaint': complaint
    }
    return render(request, 'complaint_details.html', context)

##########################--------------ADMIN VIEWS----------------------###############################

@login_required(login_url='login')

def dashboard(request):
    username = request.user.username
    return render(request, 'index.html', {'username': username})

def accept_reject_complaint(request):
    complaints = Complaint.objects.filter(status='Pending').order_by('-raised_at')
    context = {'complaints': complaints}
    return render(request, 'accept-reject complaint.html', context)

def change_status(request, complaint_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.status = status
        complaint.save()
    return redirect('accept_reject_complaint')


def assigned_success(request, complaint_id, username):
    
    return render(request, 'assigned.html', {'complaint_id': complaint_id, 'username': username})


def assign(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    users = Assign.objects.all()  # Fetch all users from the Assign model
    if request.method == 'POST':
        assigned_to_name = request.POST.get('assigned_to')  # Get the selected name from the form
        assigned_to = get_object_or_404(Assign, name=assigned_to_name)  # Retrieve the Assign instance corresponding to the selected name
        
        # Update the complaint status and assigned_to fields
        complaint.status = 'Allotted'
        complaint.assigned_to = assigned_to
        complaint.date_alloted = timezone.now()  # Set the date_alloted field to the current time
        complaint.save()
        
        # Redirect to a success page or any other page you need
        return redirect('assigned_success', complaint_id=complaint.id, username=assigned_to_name)
    
    return render(request, 'assign.html', {'complaint': complaint, 'users': users})

def table(request):
    status = request.GET.get('status')  # Get the status from the query parameters
    complaints = Complaint.objects.all()

    if status:  # If status parameter is provided, filter complaints by status
        complaints = complaints.filter(status=status)

    return render(request, 'tables.html', {'complaints': complaints, 'status_choices': STATUS_CHOICES, 'selected_status': status})

def view_file(request, file_path):
    # Get the absolute path to the file
    abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # Open the file in binary mode
    with open(abs_file_path, 'rb') as f:
        # Read the file content
        file_content = f.read()
    
    # Create a response with the file content
    response = HttpResponse(file_content, content_type='application/octet-stream')
    
    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(abs_file_path)}"'
    
    return response  

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password, backend='app1.authentication_backends.AdminBackend')
        
        if user is not None and user.is_staff:
            login(request, user)
            # Redirect authenticated staff users to a different page
            return redirect(reverse('dashboard'))  # Replace 'dashboard' with your desired URL name
        else:
            # Return an error message if authentication fails
            error_message = "Invalid username or password or user is not staff."
            return render(request, 'login.html', {'error_message': error_message})
    
    # If user is already authenticated, redirect them to the dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(reverse('/'))  # Replace 'dashboard' with your desired URL name
    
    return render(request, 'login.html')

def create_user(request):
    departments = Department.objects.all()  # Retrieve all departments
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department_id = request.POST.get('department')  # Use department ID
        
        # Retrieve the department object
        department = Department.objects.get(pk=department_id)

        # Create user
        assign = Assign.objects.create(
            name=name,
            dob=dob,
            email=email,
            phone_number=phone,
            department=department
        )
        # Redirect to a success page or login page
        return redirect('success_user')

    return render(request, 'create_user.html', {'departments': departments})

def view_users(request):
    assigns = Assign.objects.all()
    for assign in assigns:
        print(assign.id) 
    return render(request, 'view_users.html', {'assigns': assigns})

def edit_user(request, assign_id):
    assign = get_object_or_404(Assign, id=assign_id)
    departments = Department.objects.all()

    if request.method == 'POST':
        assign.name = request.POST['name']
        assign.email = request.POST['email']
        assign.phone_number = request.POST['phone_number']
        assign.department_id = request.POST['department']

        if 'profile_picture' in request.FILES:
            assign.profile_picture = request.FILES['profile_picture']

        assign.save()
        return redirect('success_user_edit')  # Redirect to a success page

    return render(request, 'edit_user.html', {'assign': assign, 'departments': departments})

def success_user(request):
    return render(request, 'success-user.html')

def success_user_edit(request):
    return render(request, 'success-user-edit.html')

def user_logout(request):
    logout(request)
    return redirect('login')

##########################--------------WORKER VIEWS----------------------###############################

def worker_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('worker_dashboard'))
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('worker_dashboard'))
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'worker_login.html')



@login_required(login_url='worker_login')
def worker_dashboard(request):
    if request.user.is_authenticated:
        try:
            current_assign = Assign.objects.get(user=request.user)
        except Assign.DoesNotExist:
            current_assign = None

        if current_assign:
            # Fetch complaints for the assigned person
            resolved_complaints = Complaint.objects.filter(assigned_to=current_assign, status='Resolved')
            pending_complaints = Complaint.objects.filter(assigned_to=current_assign, status='Allotted')
            in_progress_complaints = Complaint.objects.filter(assigned_to=current_assign, status='In Progress')

            resolved_count = resolved_complaints.count()
            pending_count = pending_complaints.count()
            in_progress_count = in_progress_complaints.count()
        else:
            resolved_complaints = []
            pending_complaints = []
            in_progress_complaints = []
            resolved_count = 0
            pending_count = 0
            in_progress_count = 0

        context = {
            'assign': current_assign,
            'resolved_count': resolved_count,
            'pending_count': pending_count,
            'in_progress_count': in_progress_count,
            'resolved_complaints': resolved_complaints,
            'pending_complaints': pending_complaints,
            'in_progress_complaints': in_progress_complaints,
        }
        return render(request, 'worker_dashboard.html', context)
    else:
        return render(request, 'worker_login.html')
    

@login_required(login_url='worker_login')
def worker_profile(request):
    try:
        assign = Assign.objects.get(user=request.user)
    except Assign.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('worker_login')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        department_id = request.POST.get('department')
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture')
        new_password = request.POST.get('password')

        if name:
            assign.name = name
        if email:
            assign.email = email
        if dob:
            try:
                assign.dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format. It must be in YYYY-MM-DD format.")
                return redirect('worker_profile')
        if department_id:
            try:
                department = Department.objects.get(id=department_id)
                assign.department = department
            except Department.DoesNotExist:
                messages.error(request, "Invalid department.")
                return redirect('worker_profile')
        if phone_number:
            assign.phone_number = phone_number
        if profile_picture:
            assign.profile_picture = profile_picture
        if new_password:
            assign.user.set_password(new_password)  # Hash the new password
            assign.user.save()
            update_session_auth_hash(request, assign.user)  # Keep the user logged in after password change

        assign.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('worker_profile')

    else:
        departments = Department.objects.all()
        return render(request, 'worker_profile.html', {'assign': assign, 'departments': departments})

@login_required(login_url='worker_login')   
def worker_resolved_complaints(request):
    current_assign = request.user.assign
    resolved_complaints = Complaint.objects.filter(assigned_to=current_assign, status='Resolved')
    
    context = {
        'resolved_complaints': resolved_complaints
    }
    
    return render(request, "worker_resolved_complaints.html", context)

@login_required(login_url='worker_login')
def worker_pending_complaints(request):
    current_assign = request.user.assign
    pending_complaints = Complaint.objects.filter(assigned_to=current_assign, status='Allotted')

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        action = request.POST.get('action')
        complaint = get_object_or_404(Complaint, id=complaint_id)

        if action == 'accept':
            complaint.status = 'In Progress'
            complaint.date_started=timezone.now()
        elif action == 'reject':
            complaint.status = 'Rejected'    
        complaint.save()

        return redirect('worker_pending_complaints')

    context = {
        'pending_complaints': pending_complaints
    }
    
    return render(request, "worker_pending_complaints.html", context)

@login_required(login_url='worker_login')
def worker_in_progress_complaints(request):
    current_assign = request.user.assign
    in_progress_complaints = Complaint.objects.filter(assigned_to=current_assign, status='In Progress')

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        action = request.POST.get('action')
        complaint = get_object_or_404(Complaint, id=complaint_id)

        if action == 'resolve':
            complaint.status = 'Resolved'
            complaint.date_resolved=timezone.now()
        elif action == 'reject':
            complaint.status = 'Rejected'
        complaint.save()

        return redirect('worker_in_progress_complaints')

    context = {
        'in_progress_complaints': in_progress_complaints
    }
    return render(request, "worker_in_progress_complaints.html",context)




@login_required(login_url='worker_login')    
def worker_success_profile(request):
    return render(request,"worker_success_profile.html")

def worker_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('worker_login')