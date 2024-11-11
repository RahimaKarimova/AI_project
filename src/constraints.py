from entities import Course, Instructor, Room, Timeslot
# constraints.py

def check_constraints(course, timeslot, room, schedule, courses, instructors):
    """Check if assigning a course to a timeslot and room satisfies all hard constraints."""
    # Get the instructor of the course being assigned
    instructor = next(inst for inst in instructors if inst.instructor_id == course.instructor_id)

    # Check if the instructor is available at the timeslot
    if timeslot.timeslot_id not in instructor.available_times:
        return False, f"Instructor {instructor.name} not available at {timeslot.timeslot_id}"

    # Check if the room is available at the timeslot
    if timeslot.timeslot_id not in room.available_times:
        return False, f"Room {room.room_id} not available at {timeslot.timeslot_id}"

    # Check if the room has enough capacity for the course
    if room.capacity < course.capacity:
        return False, f"Room {room.room_id} capacity ({room.capacity}) less than course capacity ({course.capacity})"

    # Loop through all assigned courses to check for conflicts
    for assigned_course_id, (assigned_timeslot, assigned_room) in schedule.items():
        assigned_course = next(c for c in courses if c.course_id == assigned_course_id)
        assigned_instructor = next(inst for inst in instructors if inst.instructor_id == assigned_course.instructor_id)

        # Check if the instructor is teaching another course at the same timeslot
        if assigned_timeslot.timeslot_id == timeslot.timeslot_id and assigned_instructor.instructor_id == instructor.instructor_id:
            return False, f"Instructor {instructor.name} is already teaching at {timeslot.timeslot_id}"

        # Check if the room is already occupied at the same timeslot
        if assigned_timeslot.timeslot_id == timeslot.timeslot_id and assigned_room.room_id == room.room_id:
            return False, f"Room {room.room_id} is already occupied at {timeslot.timeslot_id}"

    return True, None  # All hard constraints are satisfied


# constraints.py

def calculate_soft_constraints_score(schedule, courses, instructors):
    """Calculate individual scores for the soft constraints for each scheduled course."""
    scores = {}
    weight_break_time = -1  # Negative weight to penalize scheduling during preferred breaks
    weight_time_preference = 2  # Positive weight to reward preferred timeslots

    for course_id, (timeslot, room) in schedule.items():
        course = next(course for course in courses if course.course_id == course_id)
        instructor = next(inst for inst in instructors if inst.instructor_id == course.instructor_id)

        score = 0

        # Soft constraint: Preferred timeslot match
        if timeslot.timeslot_id in course.preferred_timeslots:
            score += weight_time_preference

        # Soft constraint: Avoid scheduling during instructor's preferred break time
        if timeslot.timeslot_id in instructor.preferred_breaks:
            score += weight_break_time

        scores[course_id] = score

    return scores
