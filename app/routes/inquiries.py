from flask import Blueprint, request, jsonify
from app.integrations.airtable.service import AirtableService
from app.integrations.airtable.models import INQUIRY_TYPE_OPTIONS, INQUIRY_STATUS_OPTIONS

inquiries = Blueprint('inquiries', __name__)
airtable = AirtableService()

@inquiries.route('/api/inquiries', methods=['POST'])
def create_inquiry():
    """Create a new inquiry"""
    data = request.json
    
    try:
        # Validate required fields
        required = ['name', 'email', 'type', 'subject', 'message']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400
            
        if data['type'] not in INQUIRY_TYPE_OPTIONS:
            return jsonify({'error': f'Invalid inquiry type. Must be one of: {INQUIRY_TYPE_OPTIONS}'}), 400
            
        # Find or create customer
        customer = airtable.find_or_create_customer({
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone', ''),
            'address': data.get('address', '')
        })
        
        # Create inquiry
        inquiry = airtable.create_inquiry(
            customer_id=customer['id'],
            inquiry_type=data['type'],
            subject=data['subject'],
            message=data['message'],
            channel=data.get('channel', 'Chat'),
            priority=data.get('priority', 'Medium')
        )
        
        return jsonify(inquiry), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inquiries.route('/api/inquiries/<inquiry_id>/status', methods=['PUT'])
def update_inquiry_status(inquiry_id):
    """Update inquiry status"""
    data = request.json
    
    try:
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
            
        if data['status'] not in INQUIRY_STATUS_OPTIONS:
            return jsonify({'error': f'Invalid status. Must be one of: {INQUIRY_STATUS_OPTIONS}'}), 400
            
        inquiry = airtable.update_inquiry_status(
            inquiry_id=inquiry_id,
            status=data['status'],
            message=data.get('message')
        )
        
        return jsonify(inquiry)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inquiries.route('/api/inquiries/<inquiry_id>/responses', methods=['POST'])
def add_inquiry_response(inquiry_id):
    """Add a response to an inquiry"""
    data = request.json
    
    try:
        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
            
        response = airtable.add_inquiry_response(
            inquiry_id=inquiry_id,
            message=data['message'],
            responder=data.get('responder', 'AI Assistant')
        )
        
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inquiries.route('/api/customers/<customer_id>/inquiries')
def get_customer_inquiries(customer_id):
    """Get all inquiries for a customer"""
    try:
        status = request.args.get('status')
        inquiries = airtable.get_customer_inquiries(customer_id, status)
        return jsonify(inquiries)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inquiries.route('/api/inquiries/<inquiry_id>/history')
def get_inquiry_history(inquiry_id):
    """Get history for an inquiry"""
    try:
        history = airtable.get_inquiry_history(inquiry_id)
        return jsonify(history)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inquiries.route('/api/inquiries/search')
def search_inquiries():
    """Search inquiries"""
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
            
        results = airtable.search_inquiries(query)
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 