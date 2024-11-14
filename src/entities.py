# entities.py

from datetime import datetime, timedelta

class Room:
    def __init__(self, room_id, capacity, version, floor, availability_dates):
        self.room_id = room_id  # Unique ID for the room
        self.capacity = capacity  # Maximum occupancy of the room
        self.version = version  # Room type (e.g., standard, deluxe, suite)
        self.floor = floor  # Floor number where the room is located
        self.availability_dates = set(availability_dates)  # Dates when the room is available
        self.booked_dates = set()  # Dates when the room is booked

    def __repr__(self):
        return (f"Room(ID: {self.room_id}, Capacity: {self.capacity}, Version: {self.version}, "
                f"Floor: {self.floor}, Available Dates: {sorted(self.availability_dates)})")

    
class Booking:
    def __init__(self, booking_id, num_guests, arrival_date, nights, room_type, preferred_floor=None):
        self.booking_id = booking_id  # Unique ID for the booking
        self.num_guests = num_guests  # Total number of guests in the booking
        self.arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d")  # Arrival date as datetime object
        self.nights = nights  # Number of nights the guest will stay
        self.departure_date = self.arrival_date + timedelta(nights)  # Departure date
        self.room_type = room_type  # Preferred room type requested by the guest
        self.preferred_floor = preferred_floor  # Preferred floor (optional)

        # Generate set of dates for the stay
        self.stay_dates = set(
            (self.arrival_date + timedelta(days=i)).date()
            for i in range(nights)
        )

    def __repr__(self):
        return (f"Booking(ID: {self.booking_id}, Guests: {self.num_guests}, Arrival: {self.arrival_date.date()}, "
                f"Nights: {self.nights}, Room Type: {self.room_type}, Preferred Floor: {self.preferred_floor})")
