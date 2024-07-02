from django.utils import timezone
from django.core.management.base import BaseCommand
from app1.models import Complaint, Department
import random
import string
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Add 10 complaints with different statuses and random dates to the database'

    def handle(self, *args, **kwargs):
        statuses = ['Accepted', 'Allotted', 'In Progress', 'Resolved','Pending', 'Rejected']
        complaints_data = []

        for _ in range(10):
            department_name = random.choice([
                'Information Technology Department',
                'Facilities Management Department',
                'Student Services Department'
            ])
            status = random.choice(statuses)
            random_date = timezone.make_aware(datetime(2024, random.randint(1, 4), random.randint(1, 28)))
            complaint_data = {
                'title': 'Sample Complaint',
                'description': 'This is a sample complaint.',
                'department_name': department_name,
                'raised_by': 'User' + ''.join(random.choices(string.ascii_uppercase, k=3)),
                'resolution_time': random.choice(['Normal', 'Immediate']),
                'status': status,
                'assigned_to': None,
                'date_raised': random_date
            }
            complaints_data.append(complaint_data)

        for data in complaints_data:
            department_name = data['department_name']
            department = Department.objects.get(name=department_name)
            complaint = Complaint(
                title=data['title'],
                description=data['description'],
                department=department,
                raised_by=data['raised_by'],
                resolution_time=data['resolution_time'],
                status=data['status'],
                assigned_to=data['assigned_to'],
                raised_at=data['date_raised']
            )
            complaint.save()

        self.stdout.write(self.style.SUCCESS('Successfully added 10 complaints with different statuses and random dates to the database'))
