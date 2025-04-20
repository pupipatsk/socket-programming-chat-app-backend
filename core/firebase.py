import firebase_admin
from firebase_admin import credentials, auth
from core.config import FIREBASE_CERT_PATH, FIREBASE_CREDENTIAL
import os
import json

firebase_key_path = FIREBASE_CERT_PATH
firebase_key_env = FIREBASE_CREDENTIAL

if firebase_key_env:
    # Step 1: Parse the string into a dictionary
    cred_dict = json.loads(firebase_key_env)

    # Step 2: Fix the private_key newlines
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    # Step 3: Pass it to Firebase
    cred = credentials.Certificate(cred_dict)
elif firebase_key_path and os.path.exists(firebase_key_path):
    cred = credentials.Certificate(firebase_key_path)
else:
    raise Exception("No Firebase credentials found.")
#cred = credentials.Certificate(FIREBASE_CERT_PATH)
firebase_admin.initialize_app(cred)

# def verify_token(id_token: str):
#     try:
#         decoded = auth.verify_id_token(id_token)
#         return decoded
#     except Exception:
#         return None


def verify_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        print("🔥 Firebase token verification failed:", str(e))
        return None
