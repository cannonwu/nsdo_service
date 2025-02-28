from flask import Blueprint, request, jsonify
import logging
from email_service import send_email
from config import WEBHOOK_SECRET

webhook_blueprint = Blueprint("webhook", __name__)

@webhook_blueprint.route("/tally-webhook", methods=["POST"])
def webhook():
    """Handles webhook requests and triggers email notifications."""
    try:
        # Validate API Key
        api_key = request.headers.get("X-Webhook-Secret")
        if not api_key or api_key != WEBHOOK_SECRET:
            logging.warning("Unauthorized webhook request")
            return jsonify({"error": "Unauthorized"}), 403

        logging.info("Received authenticated webhook request")

        # Parse JSON payload
        payload = request.get_json()
        logging.info(f"Payload received: {payload}")

        if not payload:
            logging.error("Invalid payload received")
            return jsonify({"error": "Invalid payload"}), 400

        # Extract necessary information
        data = payload.get("data", {})
        fields = data.get("fields", [])

        recipient_email = None
        recipient_name = ""
        appointment_date = None
        appointment_time = None

        for field in fields:
            if field.get("label") == "Patient Email":
                recipient_email = field.get("value")
            elif field.get("label") == "Patient Name (optional, easier for tracking later)":
                recipient_name = field.get("value", "")
            elif field.get("label") == "Appointment Date":
                appointment_date = field.get("value")
            elif field.get("label") == "Appointment Time":
                appointment_time = field.get("value")

        logging.info(f"Extracted fields - Email: {recipient_email}, Name: {recipient_name}, Date: {appointment_date}, Time: {appointment_time}")

        # Validate required fields
        if not recipient_email or not appointment_date or not appointment_time:
            logging.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        # Send email
        email_status = send_email(recipient_email, recipient_name, appointment_date, appointment_time)

        if email_status:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Failed to send email"}), 500

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500
