from rest_framework import serializers
from .models import Room, Complaint
from django.db import models

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('qr_code', 'qr_code_id')

class ComplaintCreateSerializer(serializers.ModelSerializer):
    qr_code_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Complaint
        fields = [
            'qr_code_id', 'issue_type', 'description', 'priority', 'image'
        ]

    def create(self, validated_data):
        qr_code_id = validated_data.pop('qr_code_id')
        try:
            room = Room.objects.get(qr_code_id=qr_code_id)
        except Room.DoesNotExist:
            raise serializers.ValidationError("Invalid QR code.")
        complaint = Complaint.objects.create(
            bed_number=room.bed_no,
            block=room.Block,
            room_number=room.room_no,
            floor=room.Floor_no,
            ward=room.ward,
            speciality=room.speciality,
            room_type=room.room_type,
            room_status=room.status,
            **validated_data
        )
        return complaint

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            'ticket_id', 'bed_number', 'block', 'room_number', 'floor', 'ward', 'speciality', 'room_type', 'room_status',
            'issue_type', 'description', 'priority', 'image', 'status', 'submitted_at', 'assigned_department',
            'resolved_by', 'resolved_at', 'remarks', 'submitted_by'
        ]
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