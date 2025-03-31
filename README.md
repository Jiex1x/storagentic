# Storage Booking System

A Flask-based storage booking system that integrates with Airtable for data storage and Google Calendar for appointment management.

## Features

- Customer management through Airtable
- Booking creation and management
- Google Calendar integration for appointment scheduling
- RESTful API endpoints
- Modern web interface

## Prerequisites

- Python 3.9+
- Flask
- Airtable account and API key
- Google Calendar API credentials

## Environment Variables

The following environment variables are required:

```bash
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1
GOOGLE_CALENDAR_ID=primary
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd storage-booking-system
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Google Calendar credentials:
- Place your `credentials.json` file in the project root
- Run the application and complete the OAuth flow

5. Set up Airtable:
- Create the required tables (Customers, Bookings, Inquiries, Inquiry_History)
- Set the environment variables with your Airtable credentials

## Running the Application

```bash
flask run --port 5001
```

## API Endpoints

- `GET /booking/available-slots`: Get available booking slots
- `POST /booking/create`: Create a new booking
- More endpoints documented in the code

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 