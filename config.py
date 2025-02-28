import os
import logging

# Load environment variables
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
FROM_EMAIL = os.environ['FROM_EMAIL']  # Change to your verified sender
SUPABASE_KEY = os.environ['SUPABASE_KEY']
SUPABASE_URL = os.environ['SUPABASE_URL']
SENTRY_DSN = os.environ['SENTRY_DSN']
WEBHOOK_SECRET = os.environ['WEBHOOK_SECRET']

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
