from django.contrib import admin
from .models import Room, Complaint

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_no', 'bed_no', 'Block', 'Floor_no', 'ward', 'speciality', 'room_type', 'status',)
    list_filter = ('status', 'Block', 'Floor_no', 'ward', 'speciality', 'room_type')
    search_fields = ('room_no', 'bed_no', 'Block', 'ward')
    ordering = ('Block', 'Floor_no', 'room_no')
    readonly_fields = ('qr_code', 'qr_code_id')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_id', 'room_number', 'bed_number', 'block',
        'issue_type', 'priority', 'status', 'submitted_at'
    )
    list_filter = ('status', 'priority', 'issue_type', 'block', 'ward')
    search_fields = ('ticket_id', 'room_number', 'bed_number', 'description')
    readonly_fields = ('ticket_id', 'submitted_at', 'resolved_at')
    ordering = ('-submitted_at',)
    date_hierarchy = 'submitted_at'
