import jwt
from datetime import datetime, timedelta,timezone

SECRET_KEY = "your-secret-here"
ALGORITHM = "HS256"

def create_access_token(user_id: int, expires_minutes: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)