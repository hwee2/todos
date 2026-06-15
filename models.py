from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database.orm import Base
# Todo 모델 정의
class Todo(Base):
    __tablename__ = 'todo' # 테이블 이름

    id : Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)

    title : Mapped[String] = mapped_column(String(255), nullable=False)

    is_done : Mapped[Boolean] = mapped_column(Boolean,nullable=False,default=False)

