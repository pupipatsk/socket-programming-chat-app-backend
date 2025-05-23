from dotenv import load_dotenv
import os

load_dotenv(override=True)  # Loads variables from .env into os.environ

MONGODB_URI = os.getenv("MONGODB_URI")
FIREBASE_CERT_PATH = os.getenv("FIREBASE_CERT_PATH")
FIREBASE_CREDENTIAL = os.getenv("FIREBASE_CREDENTIAL")