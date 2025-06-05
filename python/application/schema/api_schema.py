from http import HTTPStatus
from typing import Optional
from pydantic import BaseModel

# 요청
class APIRequest(BaseModel):
    query: str

# 응답
class APIResponse(BaseModel):
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