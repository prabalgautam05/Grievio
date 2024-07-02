from django.shortcuts import render, HttpResponse, redirect
from .models import Complaint, Department, Assign
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
 


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
    complaint = Complaint.objects.get(id=complaint_id)
    users = Assign.objects.all()  # Fetch all users from the Assign model
    if request.method == 'POST':
        assigned_to_name = request.POST.get('assigned_to')  # Get the selected name from the form
        assigned_to = Assign.objects.get(name=assigned_to_name)  # Retrieve the Assign instance corresponding to the selected name
        complaint.status = 'Allotted'
        complaint.assigned_to = assigned_to
        complaint.save()
        # Redirect to assigned.html
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
    if request.method == 'POST':
        email = request.POST.get('email')
        id = request.POST.get('id')
        user = authenticate(request, email=email, id=id)
        if user is not None:
            login(request, user, backend='app1.authentication_backends.AssignBackend')
            return redirect('worker_dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'worker_login.html')

@login_required
def worker_dashboard(request):
    user = request.user
    try:
        worker = Assign.objects.get(email=user.email)
    except Assign.DoesNotExist:
        worker = None

    context = {
        'worker': worker
    }
    return render(request, 'worker_dashboard.html', context)