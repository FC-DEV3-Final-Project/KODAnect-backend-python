from http import HTTPStatus
from datetime import datetime
from python.usecase.rag_chain import get_query_validation_chain, get_org_chart_chain
from python.application.schema.api_schema import APIRequest, APIResponse


async def search_org_chart(query: str) -> dict:
    query_validation_chain = get_query_validation_chain()
    query_validation_response = await query_validation_chain.ainvoke(query)

    # 현재 시간 조회
    time = get_current_time()

    if query_validation_response["is_valid"]:
        org_chart_chain = await get_org_chart_chain()
        org_chart_response = await org_chart_chain.ainvoke(query)

        message = format_message(org_chart_response)

        return APIResponse.success_response(HTTPStatus.OK, "챗봇 응답 성공", {"message": message, "time": time})
    else:
        return APIResponse.success_response(HTTPStatus.OK, "질문 유효성 필터링", {"message": query_validation_response['reason'], "time": time})


# 관련 부서 조회 여부 확인 후 챗봇 메시지 포맷팅
def format_message(response: dict):
    if response["is_exist"]:
        return f"부서: {response['dept']}, 전화번호: {response['tel_no']}"
    else:
        return response["message"]


# 현재 시간 출력 및 포맷팅(ex. 오후 04:17)
def get_current_time():
    now = datetime.now()
    period = "오전" if now.hour < 12 else "오후"  # 오전/오후
    hour_12 = now.hour % 12 if now.hour != 0 else 12  # 12시간제로 변경

    return f"{period} {hour_12:02d}:{now.minute:02d}"
