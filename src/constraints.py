from entities import Room, Booking

def check_constraints(booking, room, rooms):
    print(f"Booking type: {type(booking)}")  # Should be <class 'Booking'>
    print(f"Room type: {type(room)}")        # Should be <class 'Room'>
    """Check if assigning a booking to a room satisfies all hard constraints."""
    # Check if the room is available
    if not room.availability:
        return False, f"Room {room.room_id} is not available"

    # Check if the room has enough capacity for the number of guests in the booking
    if room.capacity < booking.num_guests:
        return False, f"Room {room.room_id} capacity ({room.capacity}) is less than the number of guests ({booking.num_guests})"

    # Check if the room type matches the preferred room type in the booking
    if room.version != booking.room_type:
        return False, f"Room {room.room_id} is of type {room.version}, but {booking.room_type} was requested"

    # Additional constraint: Check if any rooms in the same floor are booked during the arrival dates
    for other_room in rooms:
        if other_room.floor == room.floor and not other_room.availability:
            return False, f"Room {room.room_id} on floor {room.floor} has conflicting availability"

    return True, None  # All hard constraints are satisfied

def calculate_soft_constraints_score(bookings, rooms):
    """Calculate scores for the soft constraints for each booking."""
    scores = {}
    weight_capacity_excess = -1  # Penalize rooms that have much higher capacity than required
    weight_floor_preference = 2  # Reward preferred floor matches if specified in booking

    for booking in bookings:
        score = 0

        # Soft constraint: Minimize unused capacity
        assigned_room = next((room for room in rooms if room.version == booking.room_type and room.availability), None)
        if assigned_room and assigned_room.capacity > booking.num_guests:
            score += weight_capacity_excess * (assigned_room.capacity - booking.num_guests)

        # Optional: Add more soft constraints if there are specific preferences (e.g., floor preference)
        scores[booking.num_guests] = score

    return scores
