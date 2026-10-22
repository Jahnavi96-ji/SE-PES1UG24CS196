
"""Manage movie show seat reservations and ticket codes."""

import json
import secrets

# Global state for the available movie shows.
shows = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a valid seat and record the result in the log."""
    if system_logs is None:
        system_logs = []

    if show_id not in shows:
        system_logs.append(f"Unknown show: {show_id}")
        return False

    show = shows[show_id]

    if (
        not isinstance(seat_number, int)
        or isinstance(seat_number, bool)
        or not 1 <= seat_number <= show["seats"]
    ):
        system_logs.append(f"Invalid seat {seat_number} for {show_id}")
        return False

    if seat_number in show["booked"]:
        system_logs.append(
            f"Seat {seat_number} already taken for {show_id}"
        )
        return False

    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True


def release_seat(show_id, seat_number):
    """Release a booked seat, returning False if it cannot be released."""
    if show_id not in shows:
        return False

    try:
        shows[show_id]["booked"].remove(seat_number)
    except ValueError:
        return False

    return True


def ticket_code(_show_id, _seat_number):
    """Generate an unpredictable ticket code."""
    return secrets.token_hex(4)


def dump_reservations(file="seats.json"):
    """Save all show reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as reservation_file:
        json.dump(shows, reservation_file, indent=2)


def load_reservations(file="seats.json"):
    """Load reservations from a JSON file."""
    with open(file, "r", encoding="utf-8") as reservation_file:
        data = json.load(reservation_file)

    if not isinstance(data, dict):
        raise ValueError("Reservation data must be a JSON object.")

    shows.clear()
    shows.update(data)


def print_seating_summary():
    """Display the number of free seats for each show."""
    for show in shows.values():
        free = show["seats"] - len(show["booked"])
        print(
            f'{show["title"]}: {free} seats free, '
            f'booked = {show["booked"]}'
        )


def main():
    """Demonstrate seat reservation operations."""
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 25)
    reserve_seat("SHOW-2", -1)
    reserve_seat("SHOW-2", "A7")
    release_seat("SHOW-2", 3)

    print("Ticket code:", ticket_code("SHOW-1", 5))

    seat_input = input(
        "Seat number to book for SHOW-2 (Enter for 4): "
    ).strip()

    try:
        seat_number = int(seat_input) if seat_input else 4
    except ValueError:
        print("Invalid input. Please enter a whole-number seat.")
        return

    reserve_seat("SHOW-2", seat_number)

    dump_reservations()
    load_reservations()
    print_seating_summary()


if __name__ == "__main__":
    main()
