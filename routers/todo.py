from fastapi import HTTPException, APIRouter, Request
from sqlalchemy import select
from starlette import status

from database.db_connection import SessionFactory
from models import Todo
from schema.request import TodoCreateRequest, TodoUpdateRequest
from schema.response import TodoResponse

router = APIRouter(tags=["Todo"])

# 전체 할 일 조회
@router.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos_handler(request: Request):
    user_id = request.session.get("user_id")
    session = SessionFactory() # 요청 단위 세션 생성
    try:
        stmt = select(Todo).where(Todo.user_id == user_id) # 전체 조회 쿼리 객체 생성
        todos = session.execute(stmt).scalars().all() # 쿼리 실행 및 결과 변환
        return todos # 결과 반환
    finally:
        session.close() # 세션 종료


# 단일 할 일 조회
@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_todo_handler(request: Request, todo_id: int):
    user_id = request.session.get("user_id")
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id) #단일 조회 쿼리 객체 생성
        todo = session.execute(stmt).scalars().first() # 쿼리 실행 및 단일 결과 선택
        if todo: # 결과 반환
            return todo
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found")
    finally:
        session.close()


#할 일 생성
@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo_handler(request: Request, body: TodoCreateRequest): # 요청 본문 매개변수로 받기
    user_id = request.session.get("user_id") # 세션에서 사용자 아이디 조회
    session = SessionFactory()
    try:
        todo = Todo( # ORM 모델 객체 생성
            title=body.title,
            is_done=body.is_done,
            user_id = user_id,  # Todo 객체 생성 시 사용자 아이디 함께 저장
        )
        session.add(todo)  # 세션에 등록
        session.commit()  # 데이터베이스에 저장
        return todo # 생성 결과 반환
    finally:
        session.close()


# 할 일 수정
@router.patch("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo_handler(request:Request, todo_id: int, body: TodoUpdateRequest):
    user_id = request.session.get("user_id")
    session = SessionFactory()
    try:
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
    finally:
        session.close()


# 할 일 삭제
@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_handler(request:Request, todo_id: int):
    user_id = request.session.get("user_id")
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = session.execute(stmt).scalars().first()
        if todo: # 조회 결과 확인
            session.delete(todo) # 삭제 대상으로 지정
            session.commit() # 변경 사항 저장
            return # 응답 반환 (본문 없음)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found") # 조회 실패 시 예외 처리
    finally:
        session.close()
