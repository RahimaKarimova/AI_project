from constraints import calculate_soft_constraints_score, check_constraints


class Scheduler:
    def __init__(self, bookings, rooms):
        self.bookings = bookings
        self.rooms = rooms
        self.schedule = {}  # Current schedule during backtracking
        self.best_schedule = {}  # Best schedule found
        self.best_score = float('-inf')  # Soft constraints score of best schedule
        self.unscheduled_bookings = {}  # Bookings that couldn't be scheduled

    def assign_booking(self, booking, room):
        """Assign a booking to a given room."""
        self.schedule[booking.num_guests] = room  # Keyed by booking's guest count for uniqueness

    def backtracking_search(self):
        """Start the backtracking algorithm."""
        self.backtrack(0)

    def backtrack(self, booking_index):
        """Recursive backtracking function."""
        # Base condition: If we've checked all bookings, evaluate the current schedule
        if booking_index >= len(self.bookings):
            current_score = self.evaluate_schedule()
            if len(self.schedule) > len(self.best_schedule):
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
            elif len(self.schedule) == len(self.best_schedule) and current_score > self.best_score:
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
            return

        # Get the current booking to attempt to assign
        booking = self.bookings[booking_index]
        assigned = False

        for room in self.rooms:
            print(f"Trying Booking: {booking} in Room: {room}")
            # Call the constraint check function
            valid, reason = check_constraints(booking, room, self.rooms)
            if valid:
                # If valid, assign the booking and continue to the next booking
                self.assign_booking(booking, room)
                self.backtrack(booking_index + 1)  # Recursive call with next booking index
                # Undo the assignment to try other options
                self.schedule.pop(booking.num_guests)
                assigned = True

        # Even if we don't find a valid room, try the next booking
        self.backtrack(booking_index + 1)

        if not assigned:
            self.unscheduled_bookings[booking.num_guests] = reason or "No valid room available"

    def evaluate_schedule(self):
        """Calculate the total soft constraint score for the current schedule."""
        scores = calculate_soft_constraints_score( self.bookings, self.rooms)
        total_score = sum(scores.values())
        return total_score
        # for both of these there were 3 arguments for calculate_soft_constraint_score. it bein self.schedule.
        # i removed it bcus the functions was implemented to work with 2 arguments only. but who knows? maybe we will need it back idk
    def get_individual_scores(self):
        """Get individual soft constraint scores for the scheduled bookings."""
        return calculate_soft_constraints_score( self.bookings, self.rooms)
