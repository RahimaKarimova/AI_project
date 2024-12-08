from constraints import check_constraints, calculate_soft_constraints_score

class Scheduler:
    MAX_ATTEMPTS = 10000  # Set an upper bound on the number of attempts

    def __init__(self, bookings, rooms):
        self.bookings = bookings
        self.rooms = rooms
        self.schedule = {}  # Current partial schedule during backtracking
        self.best_schedule = {}
        self.best_score = float('-inf')
        self.unscheduled_bookings = {}
        self.max_bookings_scheduled = 0

        self.attempts = 0  # Count how many times we've attempted backtracking

    def assign_booking(self, booking, room):
        """Assign a booking to a given room."""
        self.schedule[booking.booking_id] = room
        room.booked_dates.update(booking.stay_dates)
        room.availability_dates.difference_update(booking.stay_dates)

    def release_booking(self, booking, room):
        """Release a booking from a room."""
        self.schedule.pop(booking.booking_id, None)
        room.booked_dates.difference_update(booking.stay_dates)
        room.availability_dates.update(booking.stay_dates)

    def count_future_constraints(self, next_booking_index, room):
        """Count how many future bookings can be assigned to the given room."""
        count = 0
        for i in range(next_booking_index, len(self.bookings)):
            future_booking = self.bookings[i]
            if (room.capacity >= future_booking.num_guests and 
                future_booking.stay_dates.issubset(room.availability_dates)):
                count += 1
        return count

    def calculate_immediate_soft_gain(self, booking, room):
        """Calculate the immediate soft constraint gain for assigning this booking to this room."""
        gain = 0
        if room.version == booking.room_type:
            gain += 2
        if booking.preferred_floor and room.floor == booking.preferred_floor:
            gain += 1
        return gain

    def backtracking_search(self):
        """Start the backtracking search."""
        self.backtrack(0)

    def backtrack(self, booking_index):
        # Increment attempt count
        self.attempts += 1

        # Check if we exceeded attempt limit
        if self.attempts > self.MAX_ATTEMPTS:
            # Mark all remaining bookings as unscheduled because we hit the limit
            for i in range(booking_index, len(self.bookings)):
                b = self.bookings[i]
                if b.booking_id not in self.schedule:
                    self.unscheduled_bookings[b.booking_id] = "No valid room found within attempt limit."
            return

        # Base condition: all bookings checked
        if booking_index >= len(self.bookings):
            current_score = self.evaluate_schedule()
            # Update best solution if needed
            if len(self.schedule) > self.max_bookings_scheduled:
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
                self.max_bookings_scheduled = len(self.schedule)
            elif len(self.schedule) == self.max_bookings_scheduled and current_score > self.best_score:
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
            return

        # Pruning: If even scheduling all remaining bookings cannot beat the current best, prune
        remaining_bookings = len(self.bookings) - booking_index
        potential_total = len(self.schedule) + remaining_bookings
        if potential_total <= self.max_bookings_scheduled:
            return

        # Current booking
        booking = self.bookings[booking_index]

        # Find valid rooms
        valid_rooms = []
        for room in self.rooms:
            # Each check increments attempts as well, to avoid too much repetition
            self.attempts += 1
            if self.attempts > self.MAX_ATTEMPTS:
                # Ran out of attempts during constraint checks
                for i in range(booking_index, len(self.bookings)):
                    b = self.bookings[i]
                    if b.booking_id not in self.schedule:
                        self.unscheduled_bookings[b.booking_id] = "No valid room found within attempt limit."
                return

            valid, _ = check_constraints(booking, room, self.schedule, self.bookings)
            if valid:
                valid_rooms.append(room)

        if not valid_rooms:
            # No valid room for this booking
            self.unscheduled_bookings[booking.booking_id] = "No valid room available"
            self.backtrack(booking_index + 1)
            return

        # Sort valid rooms by LCV, then by immediate soft gain
        valid_rooms.sort(key=lambda r: (self.count_future_constraints(booking_index + 1, r),
                                        -self.calculate_immediate_soft_gain(booking, r)))

        assigned = False
        for room in valid_rooms:
            self.assign_booking(booking, room)
            self.backtrack(booking_index + 1)
            self.release_booking(booking, room)
            assigned = True
            # If attempt limit reached in recursion, return to stop more searching
            if self.attempts > self.MAX_ATTEMPTS:
                return

        if not assigned:
            self.unscheduled_bookings[booking.booking_id] = "No valid assignment found after attempts."
            self.backtrack(booking_index + 1)

    def evaluate_schedule(self):
        """Calculate the total soft constraint score for the current schedule."""
        scores = calculate_soft_constraints_score(self.schedule, self.bookings)
        return sum(scores.values())

    def get_individual_scores(self):
        """Get individual soft constraint scores for the scheduled bookings."""
        return calculate_soft_constraints_score(self.schedule, self.bookings)
