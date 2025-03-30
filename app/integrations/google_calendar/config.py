"""Google Calendar Integration Configuration"""

import os
from datetime import datetime, timedelta

# Calendar settings
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'  # This file should be in the root directory
PORT = os.getenv('FLASK_RUN_PORT', '5001') 

print(f"\n🔧 Google Calendar Configuration:")
print(f"Calendar ID: {CALENDAR_ID}")
print(f"Credentials File: {CREDENTIALS_FILE}")
print(f"Port: {PORT}")
print(f"Scopes: {SCOPES}")

# Booking settings
BOOKING_DURATION = 60  # minutes
BUFFER_TIME = 15  # minutes buffer between bookings
WORKING_HOURS = {
    'start': 9,  # 9 AM
    'end': 17   # 5 PM
}

# Time slot settings
TIME_SLOT_INTERVAL = 30  # minutes
ADVANCE_BOOKING_DAYS = 14  # How many days in advance can book
MIN_BOOKING_NOTICE = 24  # Minimum hours notice required

def get_available_time_slots(start_date=None):
    """Get available time slots for the next two weeks"""
    if start_date is None:
        start_date = datetime.now() + timedelta(hours=MIN_BOOKING_NOTICE)
    
    end_date = start_date + timedelta(days=ADVANCE_BOOKING_DAYS)
    
    # This will be implemented to return actual available slots
    return {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'interval': TIME_SLOT_INTERVAL,
        'working_hours': WORKING_HOURS
    } 