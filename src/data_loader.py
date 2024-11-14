# data_loader.py

from datetime import datetime
import json
from entities import Room, Booking

def load_data(file_path):
    """Load and parse data from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def initialize_entities(data):
    """Initialize rooms and bookings from JSON data."""
    rooms = []
    for room_data in data['rooms']:
        # Convert availability dates from strings to datetime.date objects
        availability_dates = set()
        for date_str in room_data['availability_dates']:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            availability_dates.add(date_obj)
        room = Room(
            room_id=room_data['room_id'],
            capacity=room_data['capacity'],
            version=room_data['version'],
            floor=room_data['floor'],
            availability_dates=availability_dates
        )
        rooms.append(room)

    bookings = []
    for booking_data in data['bookings']:
        booking = Booking(
            booking_id=booking_data['booking_id'],
            num_guests=booking_data['num_guests'],
            arrival_date=booking_data['arrival_date'],
            nights=booking_data['nights'],
            room_type=booking_data['room_type'],
            preferred_floor=booking_data.get('preferred_floor')
        )
        bookings.append(booking)

    return rooms, bookings
