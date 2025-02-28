import logging
from datetime import datetime, timezone
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_email_record(recipient_email, recipient_name, appointment_datetime):
    """Inserts an email record into the Supabase database with a UTC timestamptz field."""
    try:
        # Data to be inserted
        data = {
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "appointment_datetime": appointment_datetime,  # Already in UTC ISO format
            "email_sent_timestamp": None  # Initially NULL
        }
        # Log the data before inserting
        logging.debug(f"Inserting email record with data: {data}")

        # Get the insert builder and log its details
        insert_builder = supabase.table("appointments").insert(data)
        logging.debug(f"Insert builder object: {insert_builder} (type: {type(insert_builder)})")

        # Execute the insert operation
        response = insert_builder.execute()
        logging.info(f"Inserted email record for {recipient_email}: {response}")

        # Log response type and raw data for debugging
        logging.debug(f"Insert response type: {type(response)}")
        logging.debug(f"Insert response data: {response.data}")

        # Extract record ID from response if available
        if response.data and isinstance(response.data, list) and len(response.data) > 0:
            record_id = response.data[0].get("id")
            logging.debug(f"Extracted record id: {record_id}")
        else:
            logging.debug("No data returned in response; record id is None")
            record_id = None

        return record_id
    except Exception as e:
        logging.error(f"Error inserting email record: {str(e)}", exc_info=True)
        return None

def update_email_timestamp(record_id):
    """Updates the email record with the timestamp of when the email was sent (in UTC)."""
    try:
        email_sent_timestamp = datetime.now(timezone.utc).isoformat()
        logging.debug(f"Updating email record {record_id} with timestamp {email_sent_timestamp}")
        response = supabase.table("appointments").update({"email_sent_timestamp": email_sent_timestamp}).eq("id", record_id).execute()
        logging.info(f"Updated email record {record_id} with timestamp {email_sent_timestamp}")
    except Exception as e:
        logging.error(f"Error updating email timestamp: {str(e)}", exc_info=True)
