import json
from entities import Room, Booking

def load_data(file_path):
    """Load and parse data from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def initialize_entities(data):
    """Initialize rooms and bookings from JSON data."""
    rooms = [Room(**room) for room in data['rooms']]
    bookings = [Booking(**booking) for booking in data['bookings']]
    return rooms, bookings

