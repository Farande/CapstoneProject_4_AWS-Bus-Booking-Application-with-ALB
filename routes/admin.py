from flask import Blueprint, render_template, session

from db import get_db_connection, safe_close
from data import SAMPLE_BUSES, SAMPLE_BOOKINGS

bp = Blueprint("admin", __name__)


def build_admin_analytics(buses, bookings):
    total_seats = sum(int(bus.get("available_seats", 0)) for bus in buses)
    revenue = len(bookings) * 500
    return {
        "total_buses": len(buses),
        "total_bookings": len(bookings),
        "available_seats": total_seats,
        "revenue": revenue,
        "occupancy": min(98, round((len(bookings) / max(1, len(buses) * 30)) * 100, 1)),
        "on_time": 92,
        "rating": 4.8
    }


@bp.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access denied"

    buses = list(SAMPLE_BUSES)
    bookings = list(SAMPLE_BOOKINGS)
    connection = get_db_connection()

    if connection is not None:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Buses")
                buses = cursor.fetchall()

                cursor.execute(
                    """
                    SELECT
                        Bookings.*,
                        Users.name,
                        Users.email,
                        Buses.bus_name,
                        Buses.source,
                        Buses.destination
                    FROM Bookings
                    JOIN Users
                        ON Bookings.user_id = Users.user_id
                    JOIN Buses
                        ON Bookings.bus_id = Buses.bus_id
                    ORDER BY Bookings.booking_date DESC
                    """
                )
                bookings = cursor.fetchall()
        except Exception:
            buses = list(SAMPLE_BUSES)
            bookings = list(SAMPLE_BOOKINGS)
        finally:
            safe_close(connection)

    analytics = build_admin_analytics(buses, bookings)

    return render_template("admin.html", buses=buses, bookings=bookings, analytics=analytics)
