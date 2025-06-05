import asyncio
from http import HTTPStatus
from python.core.util import get_current_time
from python.usecase.rag_chain import get_query_validation_chain, get_org_chart_chain
from python.application.schema.api_schema import APIResponse

# ==============================
# LangChain 실행 및 응답 생성 함수
# ==============================
async def search_org_chart(query: str):
    now = get_current_time()

    # 사용자 질의 유효성 검사 체인 호출
    query_validation_chain = get_query_validation_chain()
    # 부서 검색 체인 호출
    org_chart_chain = await get_org_chart_chain()

    # 두 체인 병렬 실행하여 답변 동시 생성
    query_validation_response, org_chart_response = await asyncio.gather(
        query_validation_chain.ainvoke(query),
        org_chart_chain.ainvoke(query)
    )

    # 질의 유효한 경우
    if query_validation_response["is_valid"]:
        message = format_message(org_chart_response)

        return APIResponse.success_response(HTTPStatus.OK, "챗봇 응답 성공", {"message": message, "time": now})
    # 질의 유효하지 않은 경우
    else:
        return APIResponse.success_response(HTTPStatus.OK, "질문 유효성 필터링", {"message": query_validation_response['reason'], "time": now})

# ==============================
# 챗봇 메시지 포맷팅 함수
# ==============================
def format_message(response: dict):
    if response["is_exist"]:
        return f"부서: {response['dept']}, 전화번호: {response['tel_no']}"
    else:
        return response["message"]
