from flask import Flask, request, jsonify
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)

# Initialize SendGrid API Client
sg = sendgrid.SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])
from_email = Email("tehcanno@gmail.com") # Change to your verified sender
to_email = To("cdubw408@gmail.com")  # Change to your recipient

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Parse the JSON payload from the request
        payload = request.get_json()

        if not payload:
            return jsonify({"error": "Invalid payload"}), 400

        # Extract necessary information from the payload
        data = payload.get("data", {})

        # Extract name and email from fields
        name = None
        email = None
        fields = data.get("fields", [])
        for field in fields:
            if field.get("label") == "Name":
                name = field.get("value")
            elif field.get("label") == "Email":
                email = field.get("value")

        # Print name and email to console
        print(f"Name: {name}")
        print(f"Email: {email}")

        # Send email using SendGrid
        if name and email:
            subject = "New Webhook Submission"
            content = Content("text/plain", f"Name: {name}\nEmail: {email}")
            mail = Mail(from_email, to_email, subject, content)

            # Get a JSON-ready representation of the Mail object
            mail_json = mail.get()

            # Send an HTTP POST request to /mail/send
            response = sg.send(mail)

            # Log the response
            print(f"SendGrid Response Status Code: {response.status_code}")
            print(f"SendGrid Response Headers: {response.headers}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
