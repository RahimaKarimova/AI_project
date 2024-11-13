class Room:
    def __init__(self, room_id, capacity, version, availability, floor):
        self.room_id = room_id  # Unique ID for the room
        self.capacity = capacity  # Maximum occupancy of the room
        self.version = version  # Room type (e.g., standard, deluxe, suite)
        self.availability = availability  # Whether the room is available (True or False)
        self.floor = floor  # Floor number where the room is located

    def __repr__(self):
        return f"Room(ID: {self.room_id}, Capacity: {self.capacity}, Version: {self.version}, Available: {self.availability}, Floor: {self.floor})"

class Booking:
    def __init__(self, num_guests, arrival_dates, room_type):
        self.num_guests = num_guests  # Total number of guests in the booking
        self.arrival_dates = arrival_dates  # List of dates the guests will stay
        self.room_type = room_type  # Preferred room type requested by the guest

    def __repr__(self):
        return f"Booking(Guests: {self.num_guests}, Dates: {self.arrival_dates}, Room Type: {self.room_type})"
