"""AWS integration: e-ticket storage in S3 and booking notifications via SNS.
All calls are wrapped so a missing/invalid AWS credential never crashes a
booking - it just skips the ticket upload / notification silently."""

import os
import boto3

AWS_REGION = "ap-south-1"
S3_BUCKET = "bus-booking-tickets-2026-neha"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:423370095540:BusBookingNotifications"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

sns = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)


def upload_ticket_to_s3(file_path, booking_id):
    s3_key = f"tickets/booking_{booking_id}.txt"
    try:
        s3.upload_file(file_path, S3_BUCKET, s3_key)
        return s3_key
    except Exception:
        return None


def save_ticket_to_s3(booking_record):
    booking_id = booking_record.get("booking_id")
    ticket_key = f"tickets/booking_{booking_id}.txt"
    ticket_content = f"""TransitFlow AI - E-Ticket
Booking ID: {booking_id}
Bus: {booking_record.get('bus_name', 'N/A')}
Route: {booking_record.get('source', 'N/A')} -> {booking_record.get('destination', 'N/A')}
Seat: {booking_record.get('seat_number', 'N/A')}
Date: {booking_record.get('booking_date', 'Today')}
Status: {booking_record.get('status', 'CONFIRMED')}
"""

    try:
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=ticket_key,
            Body=ticket_content.encode("utf-8"),
            ContentType="text/plain"
        )
        return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{ticket_key}"
    except Exception:
        return None


def send_booking_notification(booking_id, bus_name, seat_number, travel_date, amount):
    message = f"""
Bus Booking Confirmed

Booking ID: {booking_id}
Bus: {bus_name}
Seat Number: {seat_number}
Travel Date: {travel_date}
Amount: ₹{amount}

Thank you for using TransitFlow AI.
"""
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Bus Booking Confirmed",
            Message=message
        )
        return True
    except Exception:
        return False
