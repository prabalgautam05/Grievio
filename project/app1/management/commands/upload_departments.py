# myapp/management/commands/upload_departments.py
from django.core.management.base import BaseCommand
from app1.models import Department

class Command(BaseCommand):
    help = 'Upload departments to the database'

    def handle(self, *args, **options):
        # Define department names
        department_names = [
        
            'Academic Affairs Department',
            'Student Services Department',
            'Maintenance Services',
            'Facilities Management Department',
            'Information Technology Department',
            'Finance Department',
            'Human Resources Department',
        ]

        # Upload departments to the database
        for name in department_names:
            department, created = Department.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Department "{name}" uploaded successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Department "{name}" already exists'))
