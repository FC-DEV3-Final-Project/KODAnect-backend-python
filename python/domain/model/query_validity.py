from pydantic import BaseModel

# 질문 품질 필터링
class QueryValidity(BaseModel):
    is_valid: bool
    reason: str