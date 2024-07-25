from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import random
import string

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Allotted', 'Allotted'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected')
    )

    RESOLUTION_CHOICES = (
        ('Normal', 'Normal (10-15 days)'),
        ('Immediate', 'Immediate (3-4 days)'),
    )

    id = models.CharField(max_length=16, primary_key=True)  # Define id field explicitly
    title = models.CharField(max_length=200)
    Email= models.EmailField(null=False, blank=False)
    Phone_number=PhoneNumberField(max_length=13,null=False, blank=False)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    raised_by = models.CharField(max_length=100)
    raised_at = models.DateTimeField(auto_now_add=True)
    date_alloted = models.DateTimeField(null=True, blank=True)
    date_started = models.DateTimeField(null=True, blank=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    resolution_time = models.CharField(max_length=20, choices=RESOLUTION_CHOICES, default='Normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_to = models.ForeignKey('assign',on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='complaint_images/', null=False, blank=False, default=FileNotFoundError)
    
    def __str__(self):
        return f"Complaint ID: {self.pk}"

    def generate_custom_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(8, 16)))

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_custom_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
   ##########################----CREDIENTIALS-----#################
def generate_id():
    alphanumeric = string.ascii_uppercase + string.digits
    return ''.join(random.choices(alphanumeric, k=4))

class Assign(models.Model):
    id = models.CharField(max_length=4, primary_key=True, unique=True, default=generate_id)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    dob = models.DateField(null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assign', null=True, blank=True)

    class Meta:
        # Add this to prevent clashes with auth.User's groups and user_permissions
        default_related_name = 'assign_users'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id()
        
        # if not self.user:
        #     user = User(
        #         username=self.email,
        #         email=self.email,
        #         first_name=self.name.split()[0] if self.name else '',
        #         last_name=' '.join(self.name.split()[1:]) if len(self.name.split()) > 1 else '',
        #         is_active=True,  # Ensure the user is active
        #         is_staff=False
        #     )
        #     user.set_password()  # Set the default password using set_password
        #     user.save()
        #     self.user = user
        # else:
        #     # Update the existing User instance if needed
        #     self.user.email = self.email
        #     self.user.first_name = self.name.split()[0] if self.name else ''
        #     self.user.last_name = ' '.join(self.name.split()[1:]) if len(self.name.split()) > 1 else ''
        #     # Ensure password is set properly if you intend to change it
        #     self.user.set_password()  # Change password if required, ensure it's hashed properly
        #     self.user.save()
        
        # super().save(*args, **kwargs)

    def __str__(self):
        return self.email