from django.contrib import admin
from .models import Department, Complaint, Assign
from datetime import datetime
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'raised_by', 'department', 'status', 
        'resolution_time', 'raised_at', 'assigned_to', 
        'date_alloted', 'date_started', 'date_resolved'
    )
    list_filter = ('status', 'department', 'resolution_time')
    search_fields = ('title', 'description', 'raised_by', 'email')
    date_hierarchy = 'raised_at'
    readonly_fields = ('id', 'raised_at', 'date_alloted', 'date_started', 'date_resolved')
    actions = ['mark_as_resolved', 'mark_as_rejected']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('department', 'assigned_to')

    @admin.action(description='Mark selected complaints as resolved')
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='Resolved', date_resolved=datetime.now())

    @admin.action(description='Mark selected complaints as rejected')
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='Rejected', date_resolved=datetime.now())

@admin.register(Assign)
class AssignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'department', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('department',)
