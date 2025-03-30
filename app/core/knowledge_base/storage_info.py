"""Storage Unit Information Configuration"""

STORAGE_UNITS = {
    'small': {
        'size': '5x5',
        'square_feet': 25,
        'typical_use': 'Small furniture, boxes, documents, seasonal items',
        'equivalent': 'Small walk-in closet',
        'suitable_for': 'Students, single residents, small office archives'
    },
    'medium': {
        'size': '10x10',
        'square_feet': 100,
        'typical_use': 'Furniture from 2-3 rooms, appliances, large boxes',
        'equivalent': 'Standard single car garage',
        'suitable_for': 'Small families, apartment moves, small business inventory'
    },
    'large': {
        'size': '10x20',
        'square_feet': 200,
        'typical_use': 'Furniture from 3-4 rooms, large appliances, vehicles',
        'equivalent': 'Standard double car garage',
        'suitable_for': 'Large families, home renovation storage, business storage'
    }
}

STORAGE_TIPS = [
    "Make a list of items you plan to store - this will help estimate the space needed more accurately.",
    "Use uniform-sized storage boxes for more efficient space utilization.",
    "Consider insurance for valuable items.",
    "Place frequently accessed items near the entrance.",
    "Large furniture can be disassembled to save space.",
    "When choosing a storage unit, allow about 20% extra space for aisles and organization."
]

LOCATION_FEATURES = {
    'Security Features': [
        '24/7 Video Surveillance',
        'Electronic Access Control',
        'On-site Security Patrol',
        'Smoke Detectors'
    ],
    'Convenience Features': [
        'Free Hand Carts',
        'Spacious Loading Area',
        'Climate Control System',
        'Elevator Access'
    ],
    'Service Highlights': [
        'Flexible Lease Terms',
        'Online Bill Payment',
        'Professional Storage Consultation',
        'Moving Service Referrals'
    ]
} 