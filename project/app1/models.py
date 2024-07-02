from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
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
    Phone_number=PhoneNumberField(max_length=10,null=False, blank=False)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    raised_by = models.CharField(max_length=100)
    raised_at = models.DateTimeField(auto_now_add=True)
    resolution_time = models.CharField(max_length=20, choices=RESOLUTION_CHOICES, default='Normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_to = models.ForeignKey('assign',on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='complaint_images/', null=True, blank=True)
    
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dob']

    class Meta:
        # Add this to prevent clashes with auth.User's groups and user_permissions
        default_related_name = 'assign_users'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email