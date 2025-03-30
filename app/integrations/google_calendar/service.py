"""Google Calendar Service"""

import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
from . import config

class GoogleCalendarService:
    def __init__(self):
        """Initialize the Google Calendar service"""
        self.creds = None
        self.service = None
        self.timezone = pytz.timezone('America/Los_Angeles')
        print("🔄 Initializing Google Calendar service...")
        self.initialize_service()

    def initialize_service(self):
        """Initialize and authenticate the Google Calendar service"""
        try:
            print("\n🔄 Initializing Google Calendar service...")
            
            if os.path.exists('token.json'):
                print("Found existing token.json")
                self.creds = Credentials.from_authorized_user_file('token.json', config.SCOPES)

            if not self.creds or not self.creds.valid:
                print("Credentials not found or invalid, starting OAuth flow...")
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    print("Refreshing expired credentials...")
                    self.creds.refresh(Request())
                else:
                    print(f"Starting new OAuth flow with credentials from {config.CREDENTIALS_FILE}")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        config.CREDENTIALS_FILE, 
                        config.SCOPES
                    )
                    print("Running local server for OAuth...")
                    self.creds = flow.run_local_server(
                        port=5001,
                        access_type='offline',
                        prompt='consent'
                    )
                
                print("Saving new token...")
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())

            print("Building Google Calendar service...")
            self.service = build('calendar', 'v3', credentials=self.creds)
            print("✅ Google Calendar service initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing Google Calendar service: {str(e)}")
            raise

    def get_available_slots(self, start_date=None, days=14):
        """Get available time slots"""
        try:
            if start_date is None:
                start_date = datetime.now() + timedelta(hours=config.MIN_BOOKING_NOTICE)
            
            end_date = start_date + timedelta(days=days)
            
            # 获取现有预约
            events_result = self.service.events().list(
                calendarId=config.CALENDAR_ID,
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # 生成可用时间槽
            available_slots = self._generate_available_slots(start_date, end_date, events)
            
            return {
                'status': 'success',
                'slots': available_slots
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def create_booking(self, start_time, customer_info):
        """Create a new booking"""
        try:
            event = {
                'summary': f'Storage Collection - {customer_info["name"]}',
                'description': f'Collection service booking\nContact: {customer_info["contact"]}\nAddress: {customer_info["address"]}',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': (start_time + timedelta(minutes=config.BOOKING_DURATION)).isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
            }

            event = self.service.events().insert(
                calendarId=config.CALENDAR_ID,
                body=event
            ).execute()
            
            return {
                'status': 'success',
                'event_id': event['id'],
                'start_time': event['start']['dateTime'],
                'end_time': event['end']['dateTime']
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def _generate_available_slots(self, start_date, end_date, existing_events):
        """Generate available time slots considering existing events"""
        available_slots = []
        current_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        while current_date < end_date:
            # 跳过周末
            if current_date.weekday() >= 5:
                current_date += timedelta(days=1)
                continue

            # 生成当天的时间槽
            day_start = current_date.replace(
                hour=config.WORKING_HOURS['start'],
                minute=0,
                second=0,
                microsecond=0
            )
            
            day_end = current_date.replace(
                hour=config.WORKING_HOURS['end'],
                minute=0,
                second=0,
                microsecond=0
            )

            # 如果是今天，从当前时间开始
            if day_start.date() == datetime.now().date():
                current_time = datetime.now()
                if current_time > day_start:
                    day_start = current_time.replace(
                        minute=(current_time.minute // config.TIME_SLOT_INTERVAL) * config.TIME_SLOT_INTERVAL,
                        second=0,
                        microsecond=0
                    ) + timedelta(minutes=config.TIME_SLOT_INTERVAL)

            current_slot = day_start
            while current_slot < day_end:
                # 检查时间槽是否可用
                is_available = True
                slot_end = current_slot + timedelta(minutes=config.BOOKING_DURATION)
                
                # 检查是否与现有预约冲突
                for event in existing_events:
                    event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                    event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                    
                    # 添加缓冲时间
                    event_start = event_start - timedelta(minutes=config.BUFFER_TIME)
                    event_end = event_end + timedelta(minutes=config.BUFFER_TIME)
                    
                    # 检查是否有重叠
                    if not (current_slot >= event_end or slot_end <= event_start):
                        is_available = False
                        break

                if is_available:
                    available_slots.append({
                        'start': current_slot.isoformat(),
                        'end': slot_end.isoformat(),
                        'duration': config.BOOKING_DURATION
                    })

                current_slot += timedelta(minutes=config.TIME_SLOT_INTERVAL)

            current_date += timedelta(days=1)

        return available_slots 