"""Static sample data used as a fallback whenever the database is
unavailable, and as seed data when the database is first created."""

SAMPLE_BUSES = [
    {
        "bus_id": 1,
        "bus_name": "Express Travels",
        "bus_number": "MH 12 AB 2026",
        "source": "Mumbai",
        "destination": "Pune",
        "departure_time": "08:00 AM",
        "arrival_time": "12:00 PM",
        "fare": 500,
        "available_seats": 32
    },
    {
        "bus_id": 2,
        "bus_name": "GreenLine Travels",
        "bus_number": "MH 14 CD 8123",
        "source": "Mumbai",
        "destination": "Pune",
        "departure_time": "10:30 AM",
        "arrival_time": "02:30 PM",
        "fare": 650,
        "available_seats": 18
    },
    {
        "bus_id": 3,
        "bus_name": "Royal City Connect",
        "bus_number": "MH 09 EF 4421",
        "source": "Delhi",
        "destination": "Jaipur",
        "departure_time": "09:15 AM",
        "arrival_time": "01:30 PM",
        "fare": 780,
        "available_seats": 12
    },
    {
        "bus_id": 4,
        "bus_name": "Skyway Express",
        "bus_number": "MH 20 KL 9087",
        "source": "Pune",
        "destination": "Nagpur",
        "departure_time": "07:15 AM",
        "arrival_time": "01:10 PM",
        "fare": 920,
        "available_seats": 26
    },
    {
        "bus_id": 5,
        "bus_name": "Sahyadri Rider",
        "bus_number": "MH 27 MN 6741",
        "source": "Mumbai",
        "destination": "Ahmednagar",
        "departure_time": "05:45 PM",
        "arrival_time": "09:40 PM",
        "fare": 480,
        "available_seats": 20
    },
    {
        "bus_id": 6,
        "bus_name": "Karnataka Star",
        "bus_number": "KA 01 RS 3459",
        "source": "Bengaluru",
        "destination": "Mysuru",
        "departure_time": "06:30 AM",
        "arrival_time": "09:10 AM",
        "fare": 540,
        "available_seats": 28
    },
    {
        "bus_id": 7,
        "bus_name": "Sunrise Connect",
        "bus_number": "RJ 14 XY 7777",
        "source": "Jaipur",
        "destination": "Delhi",
        "departure_time": "08:40 AM",
        "arrival_time": "12:25 PM",
        "fare": 760,
        "available_seats": 16
    },
    {
        "bus_id": 8,
        "bus_name": "Harbor Line Travels",
        "bus_number": "MH 08 PQ 1122",
        "source": "Nashik",
        "destination": "Mumbai",
        "departure_time": "06:00 AM",
        "arrival_time": "09:05 AM",
        "fare": 600,
        "available_seats": 24
    },
    {
        "bus_id": 9,
        "bus_name": "Deccan Queen Travels",
        "bus_number": "MH 12 QT 5590",
        "source": "Pune",
        "destination": "Mumbai",
        "departure_time": "06:45 AM",
        "arrival_time": "10:30 AM",
        "fare": 520,
        "available_seats": 30
    },
    {
        "bus_id": 10,
        "bus_name": "Coastal Voyager",
        "bus_number": "MH 05 CV 2288",
        "source": "Mumbai",
        "destination": "Goa",
        "departure_time": "09:00 PM",
        "arrival_time": "07:30 AM",
        "fare": 1450,
        "available_seats": 22
    },
    {
        "bus_id": 11,
        "bus_name": "Konkan Breeze",
        "bus_number": "MH 43 KB 7710",
        "source": "Pune",
        "destination": "Goa",
        "departure_time": "08:30 PM",
        "arrival_time": "06:00 AM",
        "fare": 1350,
        "available_seats": 18
    },
    {
        "bus_id": 12,
        "bus_name": "Capital Cruiser",
        "bus_number": "DL 01 CC 3345",
        "source": "Delhi",
        "destination": "Chandigarh",
        "departure_time": "07:00 AM",
        "arrival_time": "01:00 PM",
        "fare": 690,
        "available_seats": 34
    },
    {
        "bus_id": 13,
        "bus_name": "Hyderabad Highway Links",
        "bus_number": "TS 09 HL 4467",
        "source": "Hyderabad",
        "destination": "Bengaluru",
        "departure_time": "10:00 PM",
        "arrival_time": "07:00 AM",
        "fare": 980,
        "available_seats": 25
    },
    {
        "bus_id": 14,
        "bus_name": "Chennai Coastal Connect",
        "bus_number": "TN 09 CC 5643",
        "source": "Chennai",
        "destination": "Bengaluru",
        "departure_time": "11:00 PM",
        "arrival_time": "06:30 AM",
        "fare": 850,
        "available_seats": 21
    },
    {
        "bus_id": 15,
        "bus_name": "Ahmedabad Gateway",
        "bus_number": "GJ 01 AG 6612",
        "source": "Ahmedabad",
        "destination": "Mumbai",
        "departure_time": "11:30 PM",
        "arrival_time": "07:00 AM",
        "fare": 890,
        "available_seats": 29
    }
]

SAMPLE_BOOKINGS = [
    {
        "booking_id": 1,
        "seat_number": 5,
        "booking_date": "25 September 2026",
        "status": "CONFIRMED",
        "bus_name": "Express Travels",
        "bus_number": "MH 12 AB 2026",
        "source": "Mumbai",
        "destination": "Pune"
    }
]

SAMPLE_NOTIFICATIONS = [
    {
        "title": "Seat confirmed",
        "message": "Your booking for Mumbai to Pune has been confirmed successfully.",
        "time": "2 mins ago",
        "type": "success"
    },
    {
        "title": "Route delay alert",
        "message": "Route 42 has a 15-minute delay due to weather monitoring.",
        "time": "18 mins ago",
        "type": "warning"
    },
    {
        "title": "Driver update",
        "message": "Driver has checked in and the bus is ready for departure.",
        "time": "1 hour ago",
        "type": "info"
    }
]

SAMPLE_DELAYS = [
    {
        "route": "Mumbai → Pune",
        "bus": "Express Travels",
        "status": "Delayed",
        "minutes": 15,
        "reason": "Traffic congestion on NH 48"
    },
    {
        "route": "Delhi → Jaipur",
        "bus": "Royal City Connect",
        "status": "On Time",
        "minutes": 0,
        "reason": "Normal operations"
    },
    {
        "route": "Bengaluru → Mysuru",
        "bus": "GreenRide Express",
        "status": "Delayed",
        "minutes": 22,
        "reason": "Weather advisory"
    }
]

SAMPLE_COMPLAINTS = [
    {
        "id": 101,
        "title": "Seat Allocation Issue",
        "category": "Service",
        "status": "In Review",
        "message": "The assigned seat was different from the ticket description."
    },
    {
        "id": 102,
        "title": "Late Arrival",
        "category": "Operational",
        "status": "Resolved",
        "message": "Bus arrived 20 minutes later than scheduled."
    }
]

SAMPLE_LOST_FOUND = [
    {
        "id": 201,
        "item": "Black backpack",
        "location": "Mumbai Terminal",
        "status": "Found",
        "owner": "Not claimed"
    },
    {
        "id": 202,
        "item": "Silver wallet",
        "location": "Pune Stop 2",
        "status": "Claimed",
        "owner": "R. Sharma"
    }
]

SAMPLE_FEEDBACK = [
    {
        "name": "Aisha Patel",
        "rating": 5,
        "comment": "Excellent trip experience and helpful customer service."
    },
    {
        "name": "Rohan Mehta",
        "rating": 4,
        "comment": "Booking process was smooth and the app was easy to use."
    }
]

SAMPLE_AI_ASSISTANT = [
    {
        "title": "Best route suggestion",
        "text": "Take the 8:00 AM Mumbai → Pune trip for lower traffic and a smoother arrival."
    },
    {
        "title": "Travel reminder",
        "text": "Arrive 20 minutes before departure to complete boarding and QR verification."
    },
    {
        "title": "Service alert",
        "text": "A weather advisory is active for the western corridor. Please keep your mobile notifications on."
    }
]

SAMPLE_ANALYTICS = {
    "revenue": "₹4,86,500",
    "occupancy": "84%",
    "bookings": 1680,
    "complaints": 42,
    "on_time": "92%",
    "rating": "4.8/5"
}


def get_sample_buses(source=None, destination=None):
    buses = list(SAMPLE_BUSES)
    source_term = (source or "").strip().lower()
    destination_term = (destination or "").strip().lower()

    if source_term:
        buses = [bus for bus in buses if bus["source"].lower() == source_term]

    if destination_term:
        buses = [bus for bus in buses if bus["destination"].lower() == destination_term]

    return buses
