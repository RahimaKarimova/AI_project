# main.py

from data_loader import load_data, initialize_entities
from scheduler import Scheduler

if __name__ == "__main__":
    # Load data
    file_path = '../data/data.json'  # Adjust this path if necessary
    data = load_data(file_path)
    courses, instructors, rooms, timeslots = initialize_entities(data)

    # Initialize Scheduler
    scheduler = Scheduler(courses, instructors, rooms, timeslots)

    # Run scheduling
    scheduler.backtracking_search()

    print("Scheduling completed!")

    print("\nScheduled Courses:")
    for course_id, (timeslot, room) in scheduler.schedule.items():
        course = next(course for course in courses if course.course_id == course_id)
        print(f"Course {course_id} ({course.name}) scheduled at {timeslot.timeslot_id} in Room {room.room_id}")

    unscheduled_course_ids = set(course.course_id for course in courses) - set(scheduler.schedule.keys())
    if unscheduled_course_ids:
        print("\nUnscheduled Courses:")
        for course_id in unscheduled_course_ids:
            course = next(course for course in courses if course.course_id == course_id)
            reason = scheduler.unscheduled_courses.get(course_id, "Unknown reason")
            print(f"Course {course_id} ({course.name}) could not be scheduled. Reason: {reason}")
    else:
        print("\nAll courses scheduled successfully.")

    # Get individual soft constraint scores
    scores = scheduler.get_individual_scores()
    print("\nSoft Constraints Scores:")
    for course_id, score in scores.items():
        course = next(course for course in courses if course.course_id == course_id)
        print(f"Course {course_id} ({course.name}): Score {score}")

    # Total soft constraints score
    total_score = sum(scores.values())
    print(f"\nTotal Soft Constraints Score: {total_score}")
