# constraints.py

def check_constraints(booking, room, schedule, bookings):
    """Check if assigning a booking to a room satisfies all hard constraints."""
    # Check if the room has enough capacity for the number of guests in the booking
    if room.capacity < booking.num_guests:
        return False, f"Room {room.room_id} capacity ({room.capacity}) is less than the number of guests ({booking.num_guests})"

    # Check if the room is available for all the booking dates
    if not booking.stay_dates.issubset(room.availability_dates):
        unavailable_dates = booking.stay_dates - room.availability_dates
        return False, f"Room {room.room_id} is not available on dates: {sorted(unavailable_dates)}"

    # All hard constraints are satisfied
    return True, None


def calculate_soft_constraints_score(schedule, bookings):
    """Calculate scores for the soft constraints for each scheduled booking."""
    scores = {}
    weight_room_type_match = 2    # Reward matching the preferred room type
    weight_floor_preference = 1   # Reward matching the preferred floor

    for booking_id, room in schedule.items():
        booking = next(b for b in bookings if b.booking_id == booking_id)
        score = 0

        # Soft constraint: Preferred room type match
        if room.version == booking.room_type:
            score += weight_room_type_match

        # Soft constraint: Preferred floor match
        if booking.preferred_floor and room.floor == booking.preferred_floor:
            score += weight_floor_preference

        scores[booking_id] = score

    return scores
