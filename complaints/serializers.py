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
    def create(self, validated_data):
        # Access images directly from request.FILES
        images_data = self.context['request'].FILES.getlist('images')
        # Remove 'images' from validated_data as it's not processed by the serializer field
        validated_data.pop('images', None) # Use .pop with a default to avoid KeyError if 'images' is somehow still there but None

        complaint = Complaint.objects.create(**validated_data)

        for image_file in images_data:
            ComplaintImage.objects.create(complaint=complaint, image=image_file)

        return complaint

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

class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image']
