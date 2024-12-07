# scheduler.py

from constraints import check_constraints, calculate_soft_constraints_score

class Scheduler:
    def __init__(self, bookings, rooms):
        self.bookings = bookings
        self.rooms = rooms
        self.schedule = {}  # Current schedule during backtracking
        self.best_schedule = {}  # Best schedule found
        self.best_score = float('-inf')  # Soft constraints score of best schedule
        self.unscheduled_bookings = {}  # Bookings that couldn't be scheduled
        self.max_bookings_scheduled = 0  # Maximum number of bookings scheduled so far

    def assign_booking(self, booking, room):
        """Assign a booking to a given room."""
        self.schedule[booking.booking_id] = room  # Keyed by booking's unique ID
        # Update the room's booked dates
        room.booked_dates.update(booking.stay_dates)
        # Remove booked dates from availability
        room.availability_dates.difference_update(booking.stay_dates)
        # Debug statement
        print(f"Assigned Booking {booking.booking_id} to Room {room.room_id}")

    def release_booking(self, booking, room):
        """Release a booking from a room (used during backtracking)."""
        self.schedule.pop(booking.booking_id, None)
        # Remove the booking dates from the room's booked dates
        room.booked_dates.difference_update(booking.stay_dates)
        # Add back the dates to availability
        room.availability_dates.update(booking.stay_dates)
        # Debug statement
        print(f"Released Booking {booking.booking_id} from Room {room.room_id}")

    def count_future_constraints(self, next_booking_index, room):
        """Count how many future bookings can be assigned to the given room."""
        count = 0
        for i in range(next_booking_index, len(self.bookings)):
            future_booking = self.bookings[i]
            if room.capacity >= future_booking.num_guests and future_booking.stay_dates.issubset(room.availability_dates):
                count += 1
        return count

    def backtracking_search(self):
        """Start the backtracking algorithm."""
        self.backtrack(0)

    def backtrack(self, booking_index):
        """Recursive backtracking function."""
        # Base condition: If we've checked all bookings, evaluate the current schedule
        if booking_index >= len(self.bookings):
            current_score = self.evaluate_schedule()
            if len(self.schedule) > self.max_bookings_scheduled:
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
                self.max_bookings_scheduled = len(self.schedule)
            elif len(self.schedule) == self.max_bookings_scheduled and current_score > self.best_score:
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
            return

        # Prune branches that cannot result in a better schedule
        remaining_bookings = len(self.bookings) - booking_index
        potential_total = len(self.schedule) + remaining_bookings
        if potential_total <= self.max_bookings_scheduled:
            return  # Cannot beat the best schedule, prune the branch

        # Get the current booking to attempt to assign
        booking = self.bookings[booking_index]
        assigned = False

        # Get valid rooms for the current booking, sorted by LCV heuristic
        valid_rooms = []
        for room in self.rooms:
            valid, reason = check_constraints(booking, room, self.schedule, self.bookings)
            if valid:
                valid_rooms.append(room)

        # Sort valid rooms by least constraining value
        valid_rooms.sort(key=lambda r: self.count_future_constraints(booking_index + 1, r))

        for room in valid_rooms:
            # Optionally remove or adjust the forward checking
            self.assign_booking(booking, room)
            self.backtrack(booking_index + 1)
            self.release_booking(booking, room)
            assigned = True

        if not assigned:
            self.unscheduled_bookings[booking.booking_id] = "No valid room available"
            # Even if not assigned, continue to the next booking
            self.backtrack(booking_index + 1)

    def evaluate_schedule(self):
        """Calculate the total soft constraint score for the current schedule."""
        scores = calculate_soft_constraints_score(self.schedule, self.bookings)
        total_score = sum(scores.values())
        return total_score

    def get_individual_scores(self):
        """Get individual soft constraint scores for the scheduled bookings."""
        return calculate_soft_constraints_score(self.schedule, self.bookings)
