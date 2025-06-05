from app.core.chain import get_org_chart_chain, get_query_validation_chain
from app.config.schema import QueryResponse
from app.utils.time import get_current_time
from http import HTTPStatus


async def search_org_chart(query: str) -> dict:
    query_validation_chain = get_query_validation_chain()
    query_validation_response = await query_validation_chain.ainvoke(query)

    # 현재 시간 조회
    time = get_current_time()

    if query_validation_response["is_valid"]:
        org_chart_chain = await get_org_chart_chain()
        org_chart_response = await org_chart_chain.ainvoke(query)

        message = format_message(org_chart_response)

        return QueryResponse.success_response(HTTPStatus.OK, "챗봇 응답 성공", {"message": message, "time": time})
    else:
        return QueryResponse.success_response(HTTPStatus.OK, "질문 유효성 필터링", {"message": query_validation_response['reason'], "time": time})


# 관련 부서 조회 여부 확인 후 챗봇 메시지 포맷팅
def format_message(response: dict):
    if response["is_exist"]:
        return f"부서: {response['dept']}, 전화번호: {response['tel_no']}"
    else:
        return response["message"]
