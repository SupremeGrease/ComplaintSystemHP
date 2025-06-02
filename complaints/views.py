from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Room, Complaint
from .serializers import RoomSerializer, ComplaintSerializer, ComplaintCreateSerializer
from django.utils import timezone

# Create your views here.

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        room = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Room.STATUS_CHOICES):
            room.status = new_status
            room.save()
            return Response({'status': 'success'})
        return Response({'status': 'error', 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_qr_code(self, request, pk=None):
        room = self.get_object()
        if not room.qr_code:
            room.save()  # This will generate the QR code
        return Response({
            'qr_code_url': request.build_absolute_uri(room.qr_code.url),
            'qr_code_id': str(room.qr_code_id)
        })

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().order_by('-submitted_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ComplaintCreateSerializer
        return ComplaintSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        complaint = self.get_object()
        new_status = request.data.get('status')
        remarks = request.data.get('remarks', '')

        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            complaint.remarks = remarks
            
            if new_status == 'resolved':
                complaint.resolved_by = request.user.username if self.request.user.is_authenticated else None
                complaint.resolved_at = timezone.now()
            
            complaint.save()
            return Response({'status': 'success'})
        return Response({'status': 'error', 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_filter = request.query_params.get('status', None)
        if status_filter in dict(Complaint.STATUS_CHOICES):
            complaints = self.queryset.filter(status=status_filter)
            serializer = self.get_serializer(complaints, many=True)
            return Response(serializer.data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        priority_filter = request.query_params.get('priority', None)
        if priority_filter in dict(Complaint.PRIORITY_CHOICES):
            complaints = self.queryset.filter(priority=priority_filter)
            serializer = self.get_serializer(complaints, many=True)
            return Response(serializer.data)
        return Response({'error': 'Invalid priority'}, status=status.HTTP_400_BAD_REQUEST)
