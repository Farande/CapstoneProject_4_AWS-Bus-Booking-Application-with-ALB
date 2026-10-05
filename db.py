"""All database connection handling lives here so every blueprint shares
the exact same (safe) behavior instead of copy-pasting connection logic."""

import pymysql

from data import SAMPLE_BUSES

DB_HOST = "foodorderdb.c9c6mkwkmeli.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "nehafarande"
DB_NAME = "BusBookingDB"
DB_PORT = 3306


def get_db_connection():
    """Returns a live connection, or None if the database can't be reached.
    connect_timeout keeps a bad network from hanging the whole request."""
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
    except Exception:
        return None


def safe_close(connection):
    """Closing a connection that has already dropped (flaky network, RDS
    idle timeout, etc.) can itself raise. That must never be allowed to
    escape a finally: block uncaught, or it turns into an unhandled 500
    even though the surrounding try/except looked complete."""
    if connection is None:
        return
    try:
        connection.close()
    except Exception:
        pass


def ensure_database_schema():
    connection = get_db_connection()
    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) DEFAULT 'user'
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Buses (
                    bus_id INT AUTO_INCREMENT PRIMARY KEY,
                    bus_name VARCHAR(255) NOT NULL,
                    bus_number VARCHAR(255) NOT NULL,
                    source VARCHAR(255) NOT NULL,
                    destination VARCHAR(255) NOT NULL,
                    departure_time VARCHAR(50),
                    arrival_time VARCHAR(50),
                    fare INT,
                    available_seats INT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Bookings (
                    booking_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    bus_id INT NOT NULL,
                    seat_number INT NOT NULL,
                    booking_date VARCHAR(255),
                    status VARCHAR(50) DEFAULT 'CONFIRMED'
                )
                """
            )

            cursor.execute("SELECT COUNT(*) AS total FROM Buses")
            if cursor.fetchone()["total"] == 0:
                for bus in SAMPLE_BUSES:
                    cursor.execute(
                        """
                        INSERT INTO Buses
                        (bus_name, bus_number, source, destination, departure_time, arrival_time, fare, available_seats)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            bus["bus_name"],
                            bus["bus_number"],
                            bus["source"],
                            bus["destination"],
                            bus["departure_time"],
                            bus["arrival_time"],
                            bus["fare"],
                            bus["available_seats"]
                        )
                    )

        connection.commit()
        return True
    except Exception:
        connection.rollback()
        return False
    finally:
        safe_close(connection)
