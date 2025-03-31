from flask import render_template, request, jsonify
from app.core import bp
from app.integrations.openai.service import OpenAIService
from app.integrations.google_calendar.service import GoogleCalendarService
from app.integrations.airtable.service import AirtableService
from datetime import datetime, timedelta
from app.core.assistant import StorageAssistant

openai_service = OpenAIService()
calendar_service = GoogleCalendarService()
airtable_service = AirtableService()

# Initialize the storage assistant
storage_assistant = StorageAssistant()

@bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@bp.route('/chat-interface')
def chat_interface():
    """Render the chat interface."""
    return render_template('chat.html')

@bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
            
        message = data['message']
        print(f"\n📩 Received message: {message}")
        
        # Get response from storage assistant
        response = storage_assistant.get_response(message)
        print(f"📤 Assistant response: {response}")
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred processing your request'
        }), 500

@bp.route('/booking/available-slots', methods=['GET'])
def get_available_slots():
    """Get available booking slots"""
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({
                'status': 'error',
                'message': 'Date is required'
            }), 400

        # Generate fixed time slots for the selected date
        time_slots = [
            f"{date_str}T09:00:00",  # 9 AM
            f"{date_str}T10:00:00",  # 10 AM
            f"{date_str}T11:00:00",  # 11 AM
            f"{date_str}T13:00:00",  # 1 PM (after lunch)
            f"{date_str}T14:00:00",  # 2 PM
            f"{date_str}T15:00:00",  # 3 PM
            f"{date_str}T16:00:00"   # 4 PM
        ]
        
        return jsonify({
            'status': 'success',
            'slots': time_slots
        })
            
    except Exception as e:
        print(f"Error getting time slots: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/booking/create', methods=['POST'])
def create_booking():
    """Create a new booking"""
    try:
        print("\n" + "="*50)
        print("🚀 STARTING NEW BOOKING CREATION")
        print("="*50)
        
        data = request.get_json()
        print(f"📥 Received data: {data}")
        
        # Initialize booking_data as None at the start
        booking_data = None
        
        # Validate required fields
        required_fields = ['start_time', 'name', 'contact']
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 400
            
        # Parse the datetime
        try:
            # Convert ISO format to datetime
            start_datetime = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
            print(f"✅ Parsed start datetime: {start_datetime.isoformat()}")
        except ValueError as e:
            error_msg = f"Invalid datetime format: {str(e)}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 400
            
        # Prepare customer data
        customer_info = {
            'Name': data['name'],
            'Address': data.get('address', '')
        }
        
        # Handle contact information
        contact = data['contact'].strip()
        if '@' in contact:
            customer_info['Email'] = contact
        else:
            customer_info['Phone'] = contact
            
        print("\n" + "-"*50)
        print("📊 STEP 1: Creating/Updating Customer")
        print(f"Customer info: {customer_info}")
        
        # Create or update customer
        try:
            customer = airtable_service.find_or_create_customer(customer_info)
            if not customer:
                raise ValueError("Failed to create/find customer")
            print(f"✅ Customer processed: {customer}")
            
            # Extract customer ID - handle both possible formats
            customer_id = customer.get('id') or customer.get('fields', {}).get('id')
            if not customer_id:
                raise ValueError("Customer ID not found in response")
                
        except Exception as e:
            error_msg = f"Failed to process customer information: {str(e)}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 500
            
        print("\n" + "-"*50)
        print("📅 STEP 2: Creating Calendar Event")
        
        # Create calendar event
        try:
            calendar_event = calendar_service.create_booking(
                start_datetime,
                {
                    'name': data['name'],
                    'contact': data['contact'],
                    'address': data.get('address', 'No address provided')
                }
            )
            print(f"✅ Calendar event created: {calendar_event}")
        except Exception as e:
            error_msg = f"Failed to create calendar event: {str(e)}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 500
            
        print("\n" + "-"*50)
        print("📝 STEP 3: Creating Airtable Booking")
        
        # Prepare booking data for Airtable
        booking_data = {
            'Customer': [customer_id],  # Use extracted customer_id
            'Start Date': start_datetime.strftime("%Y-%m-%d"),  # Airtable expects YYYY-MM-DD
            'Status': 'Scheduled',
            'Calendar Event ID': calendar_event['event_id'],
            'Notes': (
                f"Time: {start_datetime.strftime('%I:%M %p')}\n"
                f"Address: {data.get('address', 'No address provided')}\n"
                f"Contact: {data['contact']}"
            )
        }
        print(f"📋 Prepared booking data: {booking_data}")
        
        try:
            booking = airtable_service.create_booking(booking_data)
            if not booking:
                raise ValueError("No booking data returned from Airtable")
            
            booking_id = booking.get('id') or booking.get('fields', {}).get('id')
            if not booking_id:
                raise ValueError("Invalid booking data returned from Airtable")
                
            print(f"✅ Booking created: {booking}")
            print("\n✅ BOOKING CREATION COMPLETED SUCCESSFULLY")
            print("="*50)
            
            return jsonify({
                'status': 'success',
                'message': 'Booking created successfully',
                'booking_id': booking_id,
                'calendar_event_id': calendar_event['event_id']
            })
            
        except Exception as e:
            print(f"\n❌ Error creating booking in Airtable:")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")
            if booking_data:
                print(f"Booking data: {booking_data}")
            # Clean up calendar event if Airtable booking fails
            try:
                calendar_service.delete_event(calendar_event['id'])
                print(f"✅ Cleaned up calendar event: {calendar_event['id']}")
            except Exception as cleanup_error:
                print(f"⚠️ Failed to clean up calendar event: {str(cleanup_error)}")
            
            return jsonify({
                'status': 'error',
                'message': 'Failed to create booking',
                'error': str(e)
            }), 500
            
    except Exception as e:
        print(f"\n❌ Unexpected error in booking creation:")
        print(f"Error type: {type(e)}")
        print(f"Error details: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'error': str(e)
        }), 500 

