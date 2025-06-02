from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import uuid

# Create your models here.
class Room(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    
    bed_no = models.CharField(max_length=10)
    room_no = models.CharField(max_length=20)
    Block = models.CharField(max_length=10)
    Floor_no = models.IntegerField()
    ward = models.CharField(max_length=20)
    speciality = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    
    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_code_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return f"Room {self.room_no} - Bed {self.bed_no} - {self.Block}"
    
    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            ### here add qr_data=f""https.fsjbfbb ...."
            qr_data = str(self.qr_code_id) 
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code to model
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            filename = f'qr_code_{self.qr_code_id}.png'
            self.qr_code.save(filename, File(buffer), save=False)
        
        super().save(*args, **kwargs)


class Complaint(models.Model):
    ISSUE_CHOICES = [
        ('cleanliness', 'Cleanliness'),
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('other', 'Other'),
    ]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('open', 'Open'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'),('closed','Closed'),('on hold','On Hold')]

    # Auto-generated fields
    ticket_id = models.CharField(max_length=12, unique=True, editable=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Room details (copied, not related)
    bed_number = models.CharField(max_length=20)
    block = models.CharField(max_length=50)
    room_number = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    ward = models.CharField(max_length=50)
    speciality = models.CharField(max_length=100)
    room_type = models.CharField(max_length=50)
    room_status = models.CharField(max_length=10)

    # Patient input fields
    issue_type = models.CharField(max_length=50, choices=ISSUE_CHOICES)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    image = models.ImageField(upload_to='complaint_images/', null=True, blank=True)
    submitted_by = models.CharField(max_length=100, default="Patient")

    # Status tracking
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    assigned_department = models.CharField(max_length=100, blank=True, null=True)
    resolved_by = models.CharField(max_length=100, blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            # Generate ticket ID
            self.ticket_id = "SVN" + str(uuid.uuid4().int)[:5].zfill(5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.ticket_id} - Room {self.room_number} ({self.ward})"