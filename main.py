from pip._internal.cli import status_codes

from schema.response import TodoResponse
from fastapi import FastAPI, status, HTTPException

app = FastAPI()


# 할 일 저장
todos = [
    {"id": 1,"title": "FastAPI 공부하기","is_done": False},
    {"id": 2,"title": "운동하기", "is_done": False},
    {"id":3, "title" : "책 읽기", "is_done": False},
]

# 전체 할 일 조회
@app.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos_handler():
    return todos

# 단일 할 일 조회
@app.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_todo_handler(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found")