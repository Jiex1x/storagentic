# Airtable table names
CUSTOMERS_TABLE = 'Customers'
BOOKINGS_TABLE = 'Bookings'
INQUIRIES_TABLE = 'Inquiries'
INQUIRY_HISTORY_TABLE = 'Inquiry_History'

# Customer fields
CUSTOMER_FIELDS = {
    'Name': 'Single line text',
    'Email': 'Email',
    'Phone': 'Phone number',
    'Address': 'Long text',
    'Last Contact': 'Date',
    'Status': 'Single select',
    'Notes': 'Long text',
    'Inquiries': 'Link to Inquiries',
    'Bookings': 'Link to Bookings'
}
CUSTOMER_STATUS_OPTIONS = [
    'Active',
    'Inactive'
]
# Inquiry fields
INQUIRY_FIELDS = {
    'Subject': 'Single line text',
    'Customer': 'Link to Customers',
    'Type': 'Single select',
    'Message': 'Long text',
    'Status': 'Single select',
    'Priority': 'Single select',
    'Assigned to': 'Single line text',
    'Inquiries History': 'Link to Inquiries History'
}

# Inquiry History fields
INQUIRY_HISTORY_FIELDS = {
    'Log Summary': 'Single line text',
    'Inquiry': 'Link to Inquiries',
    'Action': 'Single select',
    'Message': 'Long text',
    'Created By': 'Single line text'
}

# Status options
INQUIRY_STATUS_OPTIONS = [
    'New',
    'In Progress',
    'Waiting for Customer',
    'Resolved',
    'Closed'
]

# Priority options
PRIORITY_OPTIONS = [
    'Low',
    'Medium',
    'High',
    'Urgent'
]

# Inquiry type options
INQUIRY_TYPE_OPTIONS = [
    'Storage Size Question',
    'Pricing Inquiry',
    'Availability Check',
    'Booking Request',
    'Technical Support',
    'Complaint',
    'Feedback',
    'Other'
]

# Booking fields
BOOKING_FIELDS = {
    'Booking Summary': 'Single line text',
    'Customer': 'Link to Customers',
    'Start Date': 'Date',
    'End Date': 'Date',
    'Status': 'Single select',
    'Notes': 'Long text',
    'Calendar Event ID': 'Single line text'
}

# Booking status options
BOOKING_STATUS_OPTIONS = [
    'Scheduled',
    'In Progress',
    'Completed',
    'Cancelled'
]
