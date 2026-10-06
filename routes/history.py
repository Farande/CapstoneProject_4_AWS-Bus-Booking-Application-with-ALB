from flask import Blueprint, render_template, redirect, session

from db import get_db_connection, safe_close
from data import SAMPLE_BOOKINGS

bp = Blueprint("history", __name__)


@bp.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    bookings = list(session.get("demo_bookings", []))
    connection = get_db_connection()

    if connection is not None:
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT
                    Bookings.booking_id,
                    Bookings.seat_number,
                    Bookings.booking_date,
                    Bookings.status,
                    Buses.bus_name,
                    Buses.bus_number,
                    Buses.source,
                    Buses.destination
                FROM Bookings
                JOIN Buses
                    ON Bookings.bus_id = Buses.bus_id
                WHERE Bookings.user_id=%s
                ORDER BY Bookings.booking_date DESC
                """
                cursor.execute(sql, (session["user_id"],))
                bookings = cursor.fetchall()
        except Exception:
            bookings = list(session.get("demo_bookings", SAMPLE_BOOKINGS))
        finally:
            safe_close(connection)

    if not bookings:
        bookings = list(session.get("demo_bookings", SAMPLE_BOOKINGS))

    return render_template("history.html", bookings=bookings)
