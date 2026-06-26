import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 DATABASE_URL 읽어오기
DATABASE_URL = os.getenv("DATABASE_URL")

# 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 팩토리 생성
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

# 세션 생성
def get_session():
    with SessionFactory() as session:
        yield session
