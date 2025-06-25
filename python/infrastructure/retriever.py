from python.infrastructure.llm import get_llm
from python.infrastructure.vector_store import get_vector_store
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter

# ======================================
# 기본 벡터 검색기, LLM 체인 필터 결합 함수
# ======================================
async def get_retriever():
    vector_store = await get_vector_store()
    llm = get_llm()

    # 기본 벡터 검색기 생성
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 2}
    )
    # LLM 체인 필터 생성
    llm_filter = LLMChainFilter.from_llm(llm)

    return ContextualCompressionRetriever(
        base_retriever=retriever,
        base_compressor=llm_filter
    )
