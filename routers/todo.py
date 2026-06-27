from fastapi import HTTPException, APIRouter, Request, Depends, UploadFile, File
from sqlalchemy import select
from starlette import status
from database.db_connection import SessionFactory
from models import Todo
from schema.request import TodoCreateRequest, TodoUpdateRequest
from schema.response import TodoResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt import decode_access_token
from database.db_connection import SessionFactory, get_session
from auth.jwt import decode_access_token
from pathlib import Path
import shutil
from fastapi.responses import FileResponse


router = APIRouter(tags=["Todo"])
bearer = HTTPBearer(auto_error=False)
UPLOAD_DIR = Path("uploads")

# 전체 할 일 조회
@router.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos_handler(session = Depends(get_session), authorization: HTTPAuthorizationCredentials | None = Depends(bearer)):
    user_id = None
    if authorization:
        token = authorization.credentials
        user_id = decode_access_token(token)
    # session = SessionFactory()
    # try:
    stmt = select(Todo).where(Todo.user_id == user_id)
    todos = session.execute(stmt).scalars().all()
    return todos
    # # finally:
    #     session.close()

# 단일 할 일 조회
@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_todo_handler(todo_id: int, session = Depends(get_session), authorization: HTTPAuthorizationCredentials | None = Depends(bearer)):
    user_id = None
    if authorization:
        token = authorization.credentials
        user_id = decode_access_token(token)
    # session = SessionFactory()
    #
    # try:
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id) #단일 조회 쿼리 객체 생성
    todo = session.execute(stmt).scalars().first() # 쿼리 실행 및 단일 결과 선택
    if todo: # 결과 반환
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found")
    # finally:
    #     session.close()


#할 일 생성
@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo_handler(body: TodoCreateRequest, session = Depends(get_session), authorization: HTTPAuthorizationCredentials | None = Depends(bearer)): # 요청 본문 매개변수로 받기
    user_id = None
    if authorization:
        token = authorization.credentials
        user_id = decode_access_token(token)
    # session = SessionFactory()
    # try:
    todo = Todo( # ORM 모델 객체 생성
        title=body.title,
        is_done=body.is_done,
        user_id = user_id,  # Todo 객체 생성 시 사용자 아이디 함께 저장
    )
    session.add(todo)  # 세션에 등록
    session.commit()  # 데이터베이스에 저장
    return todo # 생성 결과 반환
    # finally:
    #     session.close()


# 할 일 수정
@router.patch("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest, session = Depends(get_session), authorization: HTTPAuthorizationCredentials | None = Depends(bearer)):
    user_id = None
    if authorization:
        token = authorization.credentials
        user_id = decode_access_token(token)
    # session = SessionFactory()
    # try:
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id) # 수정 대상 조회 쿼리 객체 생성
    todo = session.execute(stmt).scalars().first()
    if todo:
        if body.title is not None:
            todo.title = body.title
        if body.is_done is not None:
            todo.is_done = body.is_done
        session.commit()
        return todo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,detail="Todo Not found"
    )
    # finally:
    #     session.close()


# 할 일 삭제
@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_handler(todo_id: int, session = Depends(get_session), authorization: HTTPAuthorizationCredentials | None = Depends(bearer)):
    user_id = None
    if authorization:
        token = authorization.credentials
        user_id = decode_access_token(token)
    # session = SessionFactory()
    # try:
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.execute(stmt).scalars().first()
    if todo: # 조회 결과 확인
        session.delete(todo) # 삭제 대상으로 지정
        session.commit() # 변경 사항 저장
        return # 응답 반환 (본문 없음)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found") # 조회 실패 시 예외 처리
    # finally:
    #     session.close()

# 파일 업로드
@router.post("/upload")
def upload_file(file: UploadFile=File(...)):
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

# 파일 다운로드
@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
