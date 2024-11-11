# scheduler.py

from constraints import check_constraints, calculate_soft_constraints_score

class Scheduler:
    def __init__(self, courses, instructors, rooms, timeslots):
        self.courses = courses
        self.instructors = instructors
        self.rooms = rooms
        self.timeslots = timeslots
        self.schedule = {}  # Current schedule during backtracking
        self.best_schedule = {}  # Best schedule found
        self.best_score = float('-inf')  # Soft constraints score of best schedule
        self.unscheduled_courses = {}  # Courses that couldn't be scheduled

    def assign_course(self, course, timeslot, room):
        """Assign a course to a given timeslot and room."""
        self.schedule[course.course_id] = (timeslot, room)

    def backtracking_search(self):
        """Start the backtracking algorithm."""
        # Start backtracking with the first course
        self.backtrack(0)
        # After backtracking, set the schedule to the best one found
        self.schedule = self.best_schedule.copy()

    def backtrack(self, course_index):
        """Recursive backtracking function."""
        if course_index >= len(self.courses):
            # All courses have been considered
            # Evaluate current schedule
            current_score = self.evaluate_schedule()
            # Update best schedule if current is better
            if len(self.schedule) > len(self.best_schedule):
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
            elif len(self.schedule) == len(self.best_schedule) and current_score > self.best_score:
                self.best_schedule = self.schedule.copy()
                self.best_score = current_score
            return

        course = self.courses[course_index]
        assigned = False

        for timeslot in self.timeslots:
            for room in self.rooms:
                # Check if assigning the course to this timeslot and room satisfies constraints
                valid, reason = check_constraints(
                    course, timeslot, room, self.schedule, self.courses, self.instructors
                )
                if valid:
                    self.assign_course(course, timeslot, room)
                    self.backtrack(course_index + 1)
                    # Undo assignment to try other possibilities
                    self.schedule.pop(course.course_id)
                    assigned = True

        # Try skipping the course
        self.backtrack(course_index + 1)
        if not assigned:
            # Record the reason why the course couldn't be scheduled
            self.unscheduled_courses[course.course_id] = reason or "No valid timeslot and room available"

    def evaluate_schedule(self):
        """Calculate the total soft constraint score for the current schedule."""
        scores = calculate_soft_constraints_score(self.schedule, self.courses, self.instructors)
        total_score = sum(scores.values())
        return total_score

    def get_individual_scores(self):
        """Get individual soft constraint scores for the scheduled courses."""
        return calculate_soft_constraints_score(self.schedule, self.courses, self.instructors)
