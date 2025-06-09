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


class ComplaintUpdateSerializer(serializers.ModelSerializer):
    images = ComplaintImageSerializer(many=True, read_only=True)
    new_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    existing_images = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Complaint
        fields = '_all_'
        read_only_fields = ('ticket_id',)

    def update(self, instance, validated_data):
        new_images = validated_data.pop('new_images', [])
        existing_images = validated_data.pop('existing_images', [])

        # Delete only the images not in the existing_images list
        if existing_images:
            instance.images.exclude(image__in=existing_images).delete()
        else:
            instance.images.all().delete()

        # Add new images
        for image_file in new_images:
            ComplaintImage.objects.create(complaint=instance, image=image_file)

        return super().update(instance,validated_data)

class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image']