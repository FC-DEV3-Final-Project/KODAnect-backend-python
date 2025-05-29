from app.config.schema import QueryRequest, QueryResponse
from app.service.org_chart_service import search_org_chart
from http import HTTPStatus
from fastapi import APIRouter

router = APIRouter()


@router.post("/chat", response_model=QueryResponse)
def search(request: QueryRequest):
    result = search_org_chart(request.query)

    if result["is_exist"]:
        data = f"부서: {result['dept']}, 전화번호: {result['tel_no']}"
        return QueryResponse.success_response(HTTPStatus.OK, "관련 부서 반환 성공", data)
    else:
        return QueryResponse.success_response(HTTPStatus.OK, "관련 부서 반환 실패", result['message'])

    # 에러가 발생할 경우도 분리하여 success 등 따로 처리
