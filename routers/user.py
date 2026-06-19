from fastapi import APIRouter, status

router = APIRouter(tags=["User"])

# 회원가입
@router.get("/users/signup", status_code=status.HTTP_201_CREATED)

def signup_user_handler():
    """
    회원가입 처리 과정
    1. 요청 데이터 검증
    2. 이메일 중복 검사
    3. 비밀번호 해시 생성
    4. User 모델 생성 후 DB 저장
    5. 응답 반환

    """
    pass