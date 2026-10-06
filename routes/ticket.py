from flask import Blueprint, render_template, session

from data import SAMPLE_BOOKINGS

bp = Blueprint("ticket", __name__)


@bp.route("/ticket/<int:booking_id>")
def ticket(booking_id):
    booking = None

    demo_bookings = list(session.get("demo_bookings", SAMPLE_BOOKINGS))
    for item in demo_bookings:
        if item.get("booking_id") == booking_id:
            booking = item
            break

    if booking is None:
        booking = SAMPLE_BOOKINGS[0]

    ticket_url = booking.get("ticket_url") or session.get("last_ticket_url")
    return render_template("ticket.html", booking=booking, ticket_url=ticket_url)
