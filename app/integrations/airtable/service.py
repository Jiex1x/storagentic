import os
from datetime import datetime, timezone
from airtable import Airtable
from .models import *
import requests

class AirtableService:
    def __init__(self):
        """Initialize Airtable service"""
        print("\n==================================================")
        print("🔄 INITIALIZING AIRTABLE SERVICE")
        print("==================================================")
        
        # Check if environment variables are set
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        
        print(f"API Key present: {'✅' if self.api_key else '❌'}")
        print(f"Base ID present: {'✅' if self.base_id else '❌'}")
        print(f"API Key: {self.api_key[:5]}...")
        print(f"Base ID: {self.base_id}")
        
        if not self.api_key or not self.base_id:
            raise ValueError("Missing Airtable credentials")
        
        print(f"\nInitializing with base_id: {self.base_id}")
        
        # Try to list all tables in the base
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f'https://api.airtable.com/v0/meta/bases/{self.base_id}/tables', headers=headers)
            if response.status_code == 200:
                print("\nAvailable tables in base:")
                tables = response.json().get('tables', [])
                for table in tables:
                    print(f"- {table.get('name')} (ID: {table.get('id')})")
            else:
                print(f"\n❌ Error listing tables: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"\n❌ Error listing tables: {str(e)}")
        
        print("\nConnecting to tables:")
        
        try:
            # Initialize tables
            print("\nConnecting to tables:")
            
            # Test connection to each table
            def test_table_access(table_name):
                try:
                    print(f"Testing access to table: {table_name}")
                    table = Airtable(self.base_id, table_name, api_key=self.api_key)
                    # Try to get one record to verify access
                    table.get_all(maxRecords=1)
                    return True
                except Exception as e:
                    print(f"❌ Error accessing {table_name}: {str(e)}")
                    return False
            
            # Initialize each table
            self.customers = Airtable(self.base_id, CUSTOMERS_TABLE, api_key=self.api_key)
            if test_table_access(CUSTOMERS_TABLE):
                print(f"✅ {CUSTOMERS_TABLE} - Access verified")
            else:
                raise ValueError(f"Could not access {CUSTOMERS_TABLE} table")
                
            self.bookings = Airtable(self.base_id, BOOKINGS_TABLE, api_key=self.api_key)
            if test_table_access(BOOKINGS_TABLE):
                print(f"✅ {BOOKINGS_TABLE} - Access verified")
            else:
                raise ValueError(f"Could not access {BOOKINGS_TABLE} table")
                
            self.inquiries = Airtable(self.base_id, INQUIRIES_TABLE, api_key=self.api_key)
            if test_table_access(INQUIRIES_TABLE):
                print(f"✅ {INQUIRIES_TABLE} - Access verified")
            else:
                raise ValueError(f"Could not access {INQUIRIES_TABLE} table")
                
            self.inquiry_history = Airtable(self.base_id, INQUIRY_HISTORY_TABLE, api_key=self.api_key)
            if test_table_access(INQUIRY_HISTORY_TABLE):
                print(f"✅ {INQUIRY_HISTORY_TABLE} - Access verified")
            else:
                raise ValueError(f"Could not access {INQUIRY_HISTORY_TABLE} table")
            
            print("\n✅ All tables initialized successfully")
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"\n❌ Error initializing tables: {str(e)}")
            print(f"Error type: {type(e)}")
            print("="*50 + "\n")
            raise
        
    def get_all_storage_units(self):
        """Get all storage units"""
        return self.storage_units.get_all()
        
    def get_available_units(self, size=None):
        """Get available storage units"""
        formula = "AND(Status='Available'"
        if size:
            formula += f", Size='{size}'"
        formula += ")"
        return self.storage_units.get_all(formula=formula)
        
    def create_booking(self, booking_data):
        """Create a new booking"""
        try:
            print("\n📝 Creating new booking:")
            print(f"Booking data received: {booking_data}")
            
            # Validate required fields based on BOOKING_FIELDS
            required_fields = ['Customer', 'Start Date']
            missing_fields = [field for field in required_fields if field not in booking_data]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
            
            # Ensure Status is set
            if 'Status' not in booking_data:
                booking_data['Status'] = 'Scheduled'
            
            # Remove any fields that are not in BOOKING_FIELDS
            valid_fields = set(BOOKING_FIELDS.keys())
            booking_data = {k: v for k, v in booking_data.items() if k in valid_fields}
            
            print(f"Final booking data prepared: {booking_data}")
            
            # Create the booking
            booking = self.bookings.insert(booking_data)
            
            if not booking:
                raise ValueError("Failed to create booking - no response from Airtable")
                
            print(f"✅ Booking created in Airtable: {booking}")
            
            # Return standardized response
            return {
                'id': booking.get('id'),
                'fields': booking.get('fields', {})
            }
            
        except Exception as e:
            print(f"\n❌ Error in create_booking:")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")
            print(f"Booking data: {booking_data}")
            raise
        
    def create_customer(self, customer_info):
        """Create a new customer record"""
        try:
            print("\n📝 Creating new customer")
            # Format dates for Airtable
            current_time = datetime.now().isoformat(timespec='seconds')
            
            # Ensure all date fields are in ISO format
            customer_data = {
                'Name': customer_info['name'],
                'Email': customer_info.get('email'),
                'Phone': customer_info.get('phone'),
                'Address': customer_info.get('address', ''),
                'Status': 'Active'
            }
            
            # Remove None values
            customer_data = {k: v for k, v in customer_data.items() if v is not None}
            
            print(f"Customer data prepared: {customer_data}")
            created = self.customers.insert(customer_data)
            print(f"✅ Customer created in Airtable: {created}")
            return created
        except Exception as e:
            print(f"\n❌ Error creating customer:")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")
            print(f"Customer info: {customer_info}")
            raise
        
    def find_customer(self, contact):
        """Find customer by email or phone"""
        try:
            if '@' in contact:
                # Search by email (exact match)
                email = contact.strip().lower()  # Normalize email
                formula = f"LOWER({{Email}}) = '{email}'"
            else:
                # Search by phone (exact match)
                phone = contact.strip()  # Normalize phone
                formula = f"{{Phone}} = '{phone}'"
            
            print(f"Searching for customer with formula: {formula}")
            try:
                results = self.customers.get_all(formula=formula)
                print(f"Search results: {results}")
                return results[0] if results else None
            except Exception as e:
                print(f"Error querying Airtable: {str(e)}")
                if '403' in str(e):
                    print("This appears to be a permissions error. Please check your Airtable API key and base access.")
                raise
        except Exception as e:
            print(f"Error finding customer: {str(e)}")
            raise
        
    def find_or_create_customer(self, customer_info):
        """Find existing customer or create new one"""
        # Normalize keys to lowercase
        customer_info = {k.lower(): v for k, v in customer_info.items()}
        try:
            contact = customer_info.get('email') or customer_info.get('phone')
            if not contact:
                raise ValueError("Either email or phone must be provided")
            
            print(f"\n👤 Looking for customer with contact: {contact}")
            existing = self.find_customer(contact)
            
            if existing:
                print(f"✅ Found existing customer: {existing}")
                # Update customer info and last contact time
                update_data = {
                    'Last Contact': datetime.now(timezone.utc).date().isoformat(),
                    'Name': customer_info.get('name', existing.get('fields', {}).get('Name')),
                    'Address': customer_info.get('address', existing.get('fields', {}).get('Address'))
                }
                
                # Only update email/phone if provided
                if customer_info.get('email'):
                    update_data['Email'] = customer_info['email']
                if customer_info.get('phone'):
                    update_data['Phone'] = customer_info['phone']
                
                print(f"📝 Updating customer with data: {update_data}")
                updated = self.customers.update(existing['id'], update_data)
                print(f"✅ Customer updated: {updated}")
                return {
                    'id': updated['id'],
                    'fields': updated['fields']
                }
            
            print("ℹ️ No existing customer found, creating new one")
            created = self.create_customer(customer_info)
            print(f"✅ New customer created: {created}")
            return {
                'id': created['id'],
                'fields': created['fields']
            }
        except Exception as e:
            print(f"\n❌ Error in find_or_create_customer:")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")
            raise
        
    def update_unit_status(self, unit_id, status):
        """Update storage unit status"""
        return self.storage_units.update(unit_id, {'Status': status})
        
    def get_customer_bookings(self, customer_id):
        """Get all bookings for a customer"""
        formula = f"Customer='{customer_id}'"
        return self.bookings.get_all(formula=formula)
        
    def create_inquiry(self, customer_id, inquiry_type, subject, message, priority='Medium'):
        """Create a new inquiry"""
        if inquiry_type not in INQUIRY_TYPE_OPTIONS:
            raise ValueError(f"Invalid inquiry type. Must be one of: {INQUIRY_TYPE_OPTIONS}")
            
        inquiry_data = {
            'Customer': [customer_id],
            'Type': inquiry_type,
            'Subject': subject,
            'Message': message,
            'Status': 'New',
            'Priority': priority,
        }
        
        inquiry = self.inquiries.insert(inquiry_data)
        
        # Record in history
        self.add_inquiry_history(inquiry['id'], 'Created', message)
        
        return inquiry
        
    def update_inquiry_status(self, inquiry_id, status, message=None):
        """Update inquiry status"""
        if status not in INQUIRY_STATUS_OPTIONS:
            raise ValueError(f"Invalid status. Must be one of: {INQUIRY_STATUS_OPTIONS}")
            
        update_data = {
            'Status': status,
            'Updated At': datetime.now().isoformat(timespec='seconds')
        }
        
        inquiry = self.inquiries.update(inquiry_id, update_data)
        
        # Record in history
        self.add_inquiry_history(inquiry_id, f"Status Updated to {status}", message)
        
        return inquiry
        
    def add_inquiry_response(self, inquiry_id, message, responder="AI Assistant"):
        """Add a response to an inquiry"""
        # Update inquiry
        self.inquiries.update(inquiry_id, {
            'Status': 'In Progress',
            'Updated At': datetime.now().isoformat(timespec='seconds')
        })
        
        # Record in history
        return self.add_inquiry_history(inquiry_id, 'Responded', message, responder)
        
    def add_inquiry_history(self, inquiry_id, action, message, created_by="System"):
        """Add an entry to inquiry history"""
        history_data = {
            'Inquiry': [inquiry_id],
            'Action': action,
            'Message': message,
            'Created By': created_by
        }
        return self.inquiry_history.insert(history_data)
        
    def get_customer_inquiries(self, customer_id, status=None):
        """Get all inquiries for a customer"""
        formula = f"Customer = '{customer_id}'"
        if status:
            if status not in INQUIRY_STATUS_OPTIONS:
                raise ValueError(f"Invalid status. Must be one of: {INQUIRY_STATUS_OPTIONS}")
            formula += f" AND Status = '{status}'"
            
        return self.inquiries.get_all(formula=formula)
        
    def get_inquiry_history(self, inquiry_id):
        """Get history for an inquiry"""
        formula = f"Inquiry = '{inquiry_id}'"
        return self.inquiry_history.get_all(formula=formula, sort=['Created At'])
        
    def search_inquiries(self, query):
        """Search inquiries by subject or message"""
        formula = f"OR(FIND(LOWER('{query}'), LOWER({{Subject}})), FIND(LOWER('{query}'), LOWER({{Message}})))"
        return self.inquiries.get_all(formula=formula) 