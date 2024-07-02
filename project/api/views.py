from rest_framework import viewsets
from app1.models import Complaint, Department
from .serializers import ComplaintSerializer, DepartmentSerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def update(self, request, *args, **kwargs):
        # Remove 'id' and 'assigned_to' from request data to prevent accidental modifications
        request.data.pop('id', None)
        request.data.pop('assigned_to', None)
        return super().update(request, *args, **kwargs)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def update(self, request, *args, **kwargs):
        # Remove 'id' from request data to prevent accidental modifications
        request.data.pop('id', None)
        return super().update(request, *args, **kwargs)
