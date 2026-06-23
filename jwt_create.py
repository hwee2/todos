import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "secret"

payload = {
    "user_id": 10,
    "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(token)
