from flask import Blueprint, render_template, request, redirect, session

from db import get_db_connection, safe_close
from data import SAMPLE_BUSES
from aws_utils import save_ticket_to_s3, send_booking_notification

bp = Blueprint("booking", __name__)


@bp.route("/book/<int:bus_id>", methods=["GET", "POST"])
def book(bus_id):
    if "user_id" not in session:
        return redirect("/login")

    bus = next((item for item in SAMPLE_BUSES if item["bus_id"] == bus_id), None)
    connection = get_db_connection()

    if connection is not None:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Buses WHERE bus_id=%s", (bus_id,))
                bus = cursor.fetchone()

                if not bus:
                    return "Bus not found"

                if request.method == "POST":
                    seat_number = request.form["seat_number"]

                    if bus["available_seats"] <= 0:
                        return "No seats available"

                    cursor.execute(
                        """
                        INSERT INTO Bookings
                        (user_id, bus_id, seat_number, status)
                        VALUES (%s, %s, %s, 'CONFIRMED')
                        """,
                        (session["user_id"], bus_id, seat_number)
                    )

                    cursor.execute(
                        """
                        UPDATE Buses
                        SET available_seats = available_seats - 1
                        WHERE bus_id=%s
                        AND available_seats > 0
                        """,
                        (bus_id,)
                    )

                    connection.commit()
                    return redirect("/history")
        except Exception:
            bus = next((item for item in SAMPLE_BUSES if item["bus_id"] == bus_id), None)
        finally:
            safe_close(connection)

    if request.method == "POST" and bus is not None:
        seat_number = request.form.get("seat_number")
        if not seat_number:
            return "Please select a seat"
        if bus["available_seats"] <= 0:
            return "No seats available"

        bus["available_seats"] = max(0, bus["available_seats"] - 1)
        booking = {
            "booking_id": len(session.get("demo_bookings", [])) + 1,
            "seat_number": int(seat_number),
            "booking_date": "Today",
            "status": "CONFIRMED",
            "bus_name": bus["bus_name"],
            "bus_number": bus["bus_number"],
            "source": bus["source"],
            "destination": bus["destination"]
        }
        session.setdefault("demo_bookings", []).append(booking)
        ticket_url = save_ticket_to_s3(booking)
        if ticket_url:
            booking["ticket_url"] = ticket_url
            session["last_ticket_url"] = ticket_url
        send_booking_notification(
            booking["booking_id"],
            booking["bus_name"],
            booking["seat_number"],
            booking["booking_date"],
            bus["fare"]
        )
        return redirect("/history")

    if not bus:
        return "Bus not found"

    return render_template("booking.html", bus=bus)
