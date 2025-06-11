from django.contrib import admin
from .models import Room, Complaint, ComplaintImage, Department, Issue_Category

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_no', 'bed_no', 'Block', 'Floor_no', 'ward', 'speciality', 'room_type', 'status',)
    list_filter = ('status', 'Block', 'Floor_no', 'ward', 'speciality', 'room_type')
    search_fields = ('room_no', 'bed_no', 'Block', 'ward')
    ordering = ('Block', 'Floor_no', 'room_no')
    readonly_fields = ('qr_code',)

class ComplaintImageInline(admin.TabularInline):
    model = ComplaintImage
    extra = 1

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    inlines = [ComplaintImageInline]
    list_display = (
        'ticket_id', 'room_number', 'bed_number', 'block',
        'issue_type', 'priority', 'status', 'submitted_at'
    )
    list_filter = ('status', 'priority', 'issue_type', 'block', 'ward')
    search_fields = ('ticket_id', 'room_number', 'bed_number', 'description')
    readonly_fields = ('ticket_id', 'submitted_at', 'resolved_at')
    ordering = ('-submitted_at',)
    date_hierarchy = 'submitted_at'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_code', 'department_name','status')
    search_fields = ('department_code', 'department_name','status')

@admin.register(Issue_Category)
class IssuescatAdmin(admin.ModelAdmin):
    list_display = ('issue_category_code', 'department', 'issue_category_name', 'status')
    search_fields = ('issue_category_code', 'department__department_name', 'issue_category_name', 'status')