import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import logging
from datetime import datetime, timezone
from config import SENDGRID_API_KEY, FROM_EMAIL, SENTRY_DSN
from calendar_utils import generate_calendar_links
from utils import create_attachment
from supabase_client import insert_email_record, update_email_timestamp
import sentry_sdk

#initialize Sentry
sentry_sdk.init(SENTRY_DSN)

# Initialize SendGrid API Client
sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
from_email = Email(FROM_EMAIL)

def send_email(recipient_email, recipient_name, appointment_date, appointment_time):
    """Sends an appointment confirmation email with calendar links."""
    recipient_display_name = recipient_name if recipient_name else "Valued Patient"
    formatted_datetime = f"{appointment_date} {appointment_time}"
    try:
        subject = "Your Appointment at NuSmile Dental & Orthodontics"

        # Generate calendar links
        google_calendar_link, ics_content = generate_calendar_links(appointment_date, appointment_time)

        # Create ICS attachment
        ics_attachment = create_attachment(ics_content, "appointment.ics")

        # Convert appointment date and time to a readable format
        start_dt = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M")
        time_str = start_dt.strftime("%I:%M %p").lstrip("0")
        formatted_datetime = start_dt.strftime("%A, %B %d, %Y at ") + time_str

        # Convert appointment datetime to UTC for Supabase
        appointment_datetime_utc = start_dt.replace(tzinfo=timezone.utc).isoformat()
        
        # Insert record into Supabase before sending email
        record_id = insert_email_record(recipient_email, recipient_display_name, appointment_datetime_utc)
        
        # Email body
        email_body = f"""
        <html>
        <body>
            <p>Hi {recipient_display_name},</p>
            <p>Your appointment on <strong>{formatted_datetime}</strong> at NuSmile Dental & Orthodontics is set! We look forward to your visit.</p>
            <p>For any questions, please call or text us at <a href="tel:+14082662800">(408) 266-2800</a>.</p>
            <p><strong>Location:</strong><br>
            1319 Blossom Hill Rd<br>
            San Jose, CA 95118</p>

            <p>📅 <strong>Add to Calendar:</strong></p>
            <ul>
                <li><a href="{google_calendar_link}" target="_blank">Google Calendar</a></li>
                <li>Other Calendars: Open the attached <em>appointment.ics</em> file to add the event to your calendar.</li>
            </ul>

            <p>Best regards,<br>NuSmile Dental & Orthodontics</p>
        </body>
        </html>
        """

        content = Content("text/html", email_body)
        mail = Mail(from_email, To(recipient_email), subject, content)
        mail.add_attachment(ics_attachment)

        # Send email
        logging.info(f"Sending email to {recipient_email}...")
        response = sg.send(mail)

        # Update Supabase record with email sent timestamp
        if record_id:
            update_email_timestamp(record_id)

        logging.info(f"SendGrid Response Status Code: {response.status_code}")
        return response.status_code
        
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        sentry_sdk.capture_exception(e)
        return None
