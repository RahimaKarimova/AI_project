# main.py

from data_loader import load_data, initialize_entities
from scheduler import Scheduler

if __name__ == "__main__":
    # Load data
    file_path = './data/data.json'  # Adjust this path if necessary
    data = load_data(file_path)
    rooms, bookings = initialize_entities(data)

    # Initialize Scheduler
    scheduler = Scheduler(bookings, rooms)

    # Run scheduling
    scheduler.backtracking_search()

    print("Scheduling completed!")

    print("\nScheduled Bookings:")
    for guest_count, room in scheduler.schedule.items():
        booking = next(booking for booking in bookings if booking.num_guests == guest_count)
        print(f"Booking for {guest_count} guests scheduled in Room {room.room_id}")

    unscheduled_booking_ids = set(booking.num_guests for booking in bookings) - set(scheduler.schedule.keys())
    if unscheduled_booking_ids:
        print("\nUnscheduled Bookings:")
        for guest_count in unscheduled_booking_ids:
            booking = next(booking for booking in bookings if booking.num_guests == guest_count)
            reason = scheduler.unscheduled_bookings.get(guest_count, "Unknown reason")
            print(f"Booking for {guest_count} guests could not be scheduled. Reason: {reason}")
    else:
        print("\nAll bookings scheduled successfully.")

    # Get individual soft constraint scores
    scores = scheduler.get_individual_scores()
    print("\nSoft Constraints Scores:")
    for guest_count, score in scores.items():
        booking = next(booking for booking in bookings if booking.num_guests == guest_count)
        print(f"Booking for {guest_count} guests: Score {score}")

    # Total soft constraints score
    total_score = sum(scores.values())
    print(f"\nTotal Soft Constraints Score: {total_score}")
