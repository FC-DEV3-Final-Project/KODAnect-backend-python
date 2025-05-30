from app.config.schema import QueryRequest, QueryResponse
from app.service.org_chart_service import search_org_chart
from fastapi import APIRouter
router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
async def search(request: QueryRequest):
    return await search_org_chart(request.query)
