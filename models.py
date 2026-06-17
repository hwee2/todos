from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.testing.pickleable import User

from database.orm import Base

# Todo 모델 정의
class Todo(Base):
    __tablename__ = 'todo' # 테이블 이름

    id : Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)

    title : Mapped[String] = mapped_column(String(255), nullable=False)

    is_done : Mapped[Boolean] = mapped_column(Boolean,nullable=False,default=False)

    user_id : Mapped[Integer] = mapped_column(Integer,ForeignKey('user.id'),nullable=True)

    user: Mapped[User] = relationship("User", back_populates="todos")

    # User 모델
    class User(Base):
        __tablename__ = 'user'

        id : Mapped[int] = mapped_column(Integer, primary_key=True)
        email : Mapped[String] = mapped_column(String(255),unique=True,index=True, nullable=False)
        hashed_password : Mapped[String] = mapped_column(String(255),nullable=False)
        created_at : Mapped[DateTime] = mapped_column(DateTime,server_default=func.now(),nullable=False)
        todos: Mapped[list["Todo"]] = relationship(back_populates="user", cascade="all, delete-orphan")
