from http import HTTPStatus
from typing import Optional
from pydantic import BaseModel

# ==============================
# API 요청 스키마
# ==============================
class APIRequest(BaseModel):
    query: str

# ==============================
# API 응답 스키마
# ==============================
class APIResponse(BaseModel):
    success: bool               # 성공 여부
    code: int                   # 상태 코드
    message: str                # 상태 메시지
    data: Optional[dict] = None # 전달값

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