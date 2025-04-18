import firebase_admin
from firebase_admin import credentials, auth
from core.config import FIREBASE_CERT_PATH

cred = credentials.Certificate(FIREBASE_CERT_PATH)
firebase_admin.initialize_app(cred)

def verify_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception:
        return None