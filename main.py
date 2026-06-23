from fastapi import FastAPI, APIRouter
from database.db_connection import engine
from database.orm import Base
from routers.todo import router as todo_router
from routers.user import router as user_router
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router)
app.include_router(user_router)
#세션 미들웨어 등록
app.add_middleware(SessionMiddleware,
                   secret_key="your_secret_here") # 세션 서명에 사용할 비밀키 지정


