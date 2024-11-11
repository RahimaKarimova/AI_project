import json
import json
from entities import Course, Instructor, Room, Timeslot
def load_data(file_path):
    """Load and parse data from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def initialize_entities(data):
    """Initialize courses, instructors, rooms, and timeslots from JSON data."""
    courses = [Course(**course) for course in data['courses']]
    instructors = [Instructor(**instructor) for instructor in data['instructors']]
    rooms = [Room(**room) for room in data['rooms']]
    timeslots = [Timeslot(timeslot) for timeslot in data['timeslots']]
    return courses, instructors, rooms, timeslots
