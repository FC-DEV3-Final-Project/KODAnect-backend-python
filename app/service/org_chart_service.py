from app.core.chain import get_chain
from app.config.schema import QueryResponse
from app.utils.time import get_current_time
from http import HTTPStatus


async def search_org_chart(query: str) -> dict:
    chain = await get_chain()
    response = await chain.ainvoke(query)

    # 현재 시간 조회
    time = get_current_time()
    message = format_message(response)

    return QueryResponse.success_response(HTTPStatus.OK, "챗봇 응답 성공", {"message": message, "time": time})
    # 에러가 발생할 경우 분리하여 success 등 따로 처리


# 관련 부서 조회 여부 확인 후 챗봇 메시지 포맷팅
def format_message(response: dict):
    if response["is_exist"]:
        return f"부서: {response['dept']}, 전화번호: {response['tel_no']}"
    else:
        return response["message"]
