import base64
from sendgrid.helpers.mail import Attachment

def create_attachment(file_content, filename, file_type="text/calendar"):
    """Encode and create a SendGrid attachment."""
    encoded_content = base64.b64encode(file_content.encode()).decode()
    attachment = Attachment()
    attachment.file_content = encoded_content
    attachment.file_type = file_type
    attachment.file_name = filename
    attachment.disposition = "attachment"
    return attachment
