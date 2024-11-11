class Course:
    def __init__(self, course_id, name, instructor_id, duration, capacity, preferred_timeslots=None, preferred_rooms=None):
        self.course_id = course_id
        self.name = name
        self.instructor_id = instructor_id
        self.duration = duration
        self.capacity = capacity
        self.preferred_timeslots = preferred_timeslots or []
        self.preferred_rooms = preferred_rooms or []

    def __repr__(self):
        return f"Course({self.course_id}, {self.name}, {self.instructor_id}, Capacity: {self.capacity}, Duration: {self.duration})"


class Instructor:
    def __init__(self, instructor_id, name, available_times=None, preferred_breaks=None):
        self.instructor_id = instructor_id
        self.name = name
        self.available_times = available_times or []
        self.preferred_breaks = preferred_breaks or []

    def __repr__(self):
        return f"Instructor({self.instructor_id}, {self.name})"


class Room:
    def __init__(self, room_id, capacity, available_times=None):
        self.room_id = room_id
        self.capacity = capacity
        self.available_times = available_times or []

    def __repr__(self):
        return f"Room({self.room_id}, Capacity: {self.capacity})"


class Timeslot:
    def __init__(self, timeslot_id):
        self.timeslot_id = timeslot_id

    def __repr__(self):
        return f"Timeslot({self.timeslot_id})"
