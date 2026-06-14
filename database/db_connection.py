from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 데이터베이스 연결 정보 설정
DATABASE_URL = "mysql+pymysql://root:epqp12!@localhost:3306/fastapi_db"

# 엔진 생성
engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)