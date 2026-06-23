import jwt
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException, status


SECRET_KEY = "your-secret-here"
ALGORITHM = "HS256"

#액세스 토큰 생설
def create_access_token(user_id: int, expires_minutes: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# 액세스 토큰 검증 및 사용자 정보 추출
def decode_access_token(token: str) -> int:
    try:
        #토큰 디코딩 및 사용자 아이디 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    #토큰 만료 예외처리
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "Token expired")
    # 유효하지 않은 토큰 예외 처리
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")