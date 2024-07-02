from rest_framework import serializers
from app1.models import Complaint, Department
from django.contrib.auth.models import User

class ComplaintSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name', read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)

    class Meta:
        model = Complaint
        fields = ['id', 'title', 'description', 'department', 'raised_by', 'raised_at', 'resolution_time', 'status', 'assigned_to', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['department'] = instance.department.name
        return data

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
