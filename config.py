import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI')

if not MONGODB_URI: # Check if MONGODB_URI is not set
    raise ValueError("Missing required environment variables. Please check your .env file")