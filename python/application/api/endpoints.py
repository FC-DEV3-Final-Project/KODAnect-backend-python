from python.application.schema.api_schema import APIRequest, APIResponse
from python.domain.service.org_chart_service import search_org_chart
from fastapi import APIRouter
router = APIRouter()

# ==============================
# POST "/chat" 요청 처리
# ==============================
@router.post("/chat", response_model=APIResponse)
async def search(request: APIRequest):
    return await search_org_chart(request.query)
