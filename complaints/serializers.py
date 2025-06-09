import hmac
import hashlib
from django.conf import settings
from rest_framework import serializers
from .models import Room, Complaint, ComplaintImage
from django.db import models

class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image']  # you can also include 'id' if needed

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('qr_code', 'dataenc')

class ComplaintCreateSerializer(serializers.ModelSerializer):
    images = ComplaintImageSerializer(many=True,write_only=True,required=False)
    
    # Add fields to receive QR data and signature from frontend
    qr_data_from_qr = serializers.CharField(write_only=True, required=False)
    qr_signature_from_qr = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        # Access images directly from request.FILES
        images_data = self.context['request'].FILES.getlist('images')
        # Remove 'images' from validated_data as it's not processed by the serializer field
        validated_data.pop('images', None) 
        
        # Remove QR data and signature as they are for validation only
        validated_data.pop('qr_data_from_qr', None)
        validated_data.pop('qr_signature_from_qr', None)

        complaint = Complaint.objects.create(**validated_data)

        for image_file in images_data:
            ComplaintImage.objects.create(complaint=complaint, image=image_file)

        return complaint

    def validate(self, data):
        # Perform existing room validation first
        # Only validate room if room-related fields are being updated
        if any(field in data for field in ['bed_number', 'room_number', 'block', 'floor', 'ward', 'speciality', 'room_type']):
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
        
        # HMAC Verification Logic
        qr_data_from_qr = self.initial_data.get('qr_data_from_qr')
        qr_signature_from_qr = self.initial_data.get('qr_signature_from_qr')

        if qr_data_from_qr and qr_signature_from_qr:
            expected_signature = hmac.new(
                settings.QR_CODE_SECRET_KEY.encode('utf-8'),
                qr_data_from_qr.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, qr_signature_from_qr):
                raise serializers.ValidationError({'qr_code': 'QR code data has been tampered with or is invalid.'})
        elif not qr_data_from_qr and not qr_signature_from_qr and self.context['request'].method == 'POST':
            # If it's a POST request and QR data/signature are missing, it means
            # the request is not coming from a QR scan, so we don't apply this validation.
            pass # Allow requests without QR data/signature
        else:
             raise serializers.ValidationError({'qr_code': 'QR data or signature missing for QR-based complaint submission.'})

        return data

    class Meta:
        model = Complaint
        fields = '__all__'

   

class ComplaintSerializer(serializers.ModelSerializer):
    images = ComplaintImageSerializer(many=True, read_only=True)
    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ('ticket_id',)

    def validate(self, data):
        # Only validate room if room-related fields are being updated
        if any(field in data for field in ['bed_number', 'room_number', 'block', 'floor', 'ward', 'speciality', 'room_type']):
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


class ComplaintUpdateSerializer(serializers.ModelSerializer):
    images = ComplaintImageSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ('ticket_id',)

    def update(self, instance, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        validated_data.pop('images', None)

        # Update complaint fields
        complaint = super().update(instance, validated_data)

        # Create new images
        for image_file in images_data:
            ComplaintImage.objects.create(complaint=complaint, image=image_file)

        return complaint

class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image']