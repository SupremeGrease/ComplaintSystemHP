from rest_framework import serializers
from .models import Room, Complaint
from django.db import models

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('qr_code', 'dataenc')

class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['issue_type', 'description', 'priority', 'image']

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ('ticket_id', 'submitted_at', 'resolved_at', 'resolved_by', 'submitted_by')

    def validate(self, data):
        # Validate that room exists and is active
        try:
            room = Room.objects.get(
                bed_no=data['bed_number'],
                room_no=data['room_number'],
                Block=data['block'],
                Floor_no=data['floor'],
                ward=data['ward'],
                speciality=data['speciality'],
                room_type=data['room_type']
            )
            if room.status != 'active':
                raise serializers.ValidationError("The specified room is not active")
            # Update room_status to match room's status
            data['room_status'] = room.status
        except Room.DoesNotExist:
            raise serializers.ValidationError("Room not found with the provided details")
        return data

# Removing the duplicate Room model class that was here 