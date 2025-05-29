from pydantic import BaseModel
from typing import Optional
from http import HTTPStatus


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    success: bool
    code: int
    message: str
    data: Optional[str] = None

    @classmethod
    def success_response(cls, status: HTTPStatus, message: str, data: Optional[str] = None):
        return cls(
            success=True,
            code=status.value,
            message=message,
            data=data
        )

    @classmethod
    def fail_response(cls, status: HTTPStatus, message: str, data: Optional[str] = None):
        return cls(
            success=False,
            code=status.value,
            message=message,
            data=data
        )
