import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# IBM Watson API setup
API_KEY = os.getenv("API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

if not API_KEY:
    raise ValueError("API_KEY is missing in environment variables.")
if not MONGO_URI:
    raise ValueError("MONGO_URI is missing in environment variables.")

# IBM Watson authentication
IBM_AUTH_URL = "https://iam.cloud.ibm.com/identity/token"
IBM_API_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
