import os
import django
import json
import base64

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'complaintsystem.settings')
django.setup()

from complaints.models import Room

# Create a test room
test_room = Room(
    bed_no="101",
    room_no="A101",
    Block="A",
    Floor_no=1,
    ward="General",
    speciality="General",
    room_type="Standard",
    status="active"
)

# Get the encoded data
encoded_data = test_room.get_room_data()
print("Encoded data:", encoded_data)

# Decode and verify
decoded_json = base64.b64decode(encoded_data).decode()
decoded_data = json.loads(decoded_json)
print("\nDecoded data:", decoded_data)

# Verify all fields are present
expected_fields = ['bed_no', 'room_no', 'Block', 'Floor_no', 'ward', 'speciality', 'room_type', 'status']
missing_fields = [field for field in expected_fields if field not in decoded_data]
if missing_fields:
    print("\nMissing fields:", missing_fields)
else:
    print("\nAll fields present!")

# Verify data matches
print("\nVerifying data:")
for field in expected_fields:
    print(f"{field}: Original={getattr(test_room, field)}, Decoded={decoded_data[field]}") 