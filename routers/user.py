from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from schema.request import UserSignRequest
from database.db_connection import SessionFactory
from models import User

router = APIRouter(tags=["User"])

# 회원가입
@router.post("/users/signup", status_code=status.HTTP_201_CREATED)

def signup_user_handler(body: UserSignRequest):
    # 이메일 중복 검사
    with SessionFactory() as session:
        stmt = select(User).where(User.email == body.email)
        existing_user = session.scalars(stmt)
        if existing_user :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 이메일입니다.")
    """
    회원가입 처리 과정
    1. 요청 데이터 검증
    2. 이메일 중복 검사
    3. 비밀번호 해시 생성
    4. User 모델 생성 후 DB 저장
    5. 응답 반환

    """
    pass