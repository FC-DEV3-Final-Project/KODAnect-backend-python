from pydantic import BaseModel
from typing import Optional
from http import HTTPStatus

# 요청
class QueryRequest(BaseModel):
    query: str

# 응답
class QueryResponse(BaseModel):
    success: bool
    code: int
    message: str
    data: Optional[dict] = None

    @classmethod
    def success_response(cls, status: HTTPStatus, message: str, data: Optional[dict] = None):
        return cls(
            success=True,
            code=status.value,
            message=message,
            data=data
        )

    @classmethod
    def fail_response(cls, status: HTTPStatus, message: str, data: Optional[dict] = None):
        return cls(
            success=False,
            code=status.value,
            message=message,
            data=data
        )

# 질문 품질 필터링
class QueryValidity(BaseModel):
    is_valid: bool
    reason: str