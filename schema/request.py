from pydantic import BaseModel

# 할 일 생성 요청 모델
class TodoCreateRequest(BaseModel):
    title: str
    is_done: bool = False

