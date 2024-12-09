# main.py

from data_loader import load_data, initialize_entities
from scheduler import Scheduler
from datetime import datetime

if __name__ == "__main__":
    # Load data
    file_path = '../data/data.json'  # Adjust this path if necessary
    data = load_data(file_path)
    rooms, bookings = initialize_entities(data)

    # Initialize Scheduler
    scheduler = Scheduler(bookings, rooms)

    # Run scheduling
    scheduler.backtracking_search()

    # After backtracking, set the schedule to the best one found
    scheduler.schedule = scheduler.best_schedule.copy()

    print("Scheduling completed!")

    print("\nScheduled Bookings:")
    if scheduler.schedule:
        for booking_id, room in scheduler.schedule.items():
            booking = next(booking for booking in bookings if booking.booking_id == booking_id)
            stay_dates_str = ', '.join([date.strftime("%Y-%m-%d") for date in sorted(booking.stay_dates)])
            print(f"Reservation ID: {booking_id}")
            print(f"  Room Assigned: {room.room_id}")
            print(f"  Number of Guests: {booking.num_guests}")
            print(f"  Stay Dates: {stay_dates_str}")
            print(f"  Room Type: {room.version}")
            print(f"  Floor: {room.floor}")
            print("-" * 40)
    else:
        print("No bookings were scheduled.")

    unscheduled_booking_ids = set(booking.booking_id for booking in bookings) - set(scheduler.schedule.keys())
    if unscheduled_booking_ids:
        print("\nUnscheduled Bookings:")
        for booking_id in unscheduled_booking_ids:
            booking = next(booking for booking in bookings if booking.booking_id == booking_id)
            stay_dates_str = ', '.join([date.strftime("%Y-%m-%d") for date in sorted(booking.stay_dates)])
            reason = scheduler.unscheduled_bookings.get(booking_id, "Unknown reason")
            print(f"Reservation ID: {booking_id}")
            print(f"  Number of Guests: {booking.num_guests}")
            print(f"  Requested Stay Dates: {stay_dates_str}")
            print(f"  Room Type Preference: {booking.room_type}")
            print(f"  Preferred Floor: {booking.preferred_floor}")
            print(f"  Reason: {reason}")
            print("-" * 40)
    else:
        print("\nAll bookings scheduled successfully.")

    # Get individual soft constraint scores
    scores = scheduler.get_individual_scores()
    if scores:
        print("\nSoft Constraints Scores:")
        for booking_id, score in scores.items():
            print(f"Reservation ID: {booking_id} - Score: {score}")

        # Total soft constraints score
        total_score = sum(scores.values())
        print(f"\nTotal Soft Constraints Score: {total_score}")
    else:
        print("\nNo soft constraints scores to display.")

    # Print logs and statistics
    print("\n--- Statistics and Logs ---")
    print(f"Total Attempts: {scheduler.attempts}")
    print(f"Total Bookings: {len(bookings)}")
    print(f"Successful Bookings: {len(scheduler.schedule)}")
    print(f"Unsuccessful Bookings: {len(unscheduled_booking_ids)}")
    # print("\nFailure Reasons:")
    # for reason, count in scheduler.failure_reasons.items():
    #     print(f"  {reason}: {count}")
