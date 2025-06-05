from python.infrastructure.llm import get_llm
from python.infrastructure.vector_store import load_vector_store
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter


async def get_retriever():
    vector_store = await load_vector_store()
    llm = get_llm()

    # 벡터 저장소를 통해 retriever 생성
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )
    # LLMChainFilter 생성
    llm_filter = LLMChainFilter.from_llm(llm)

    return ContextualCompressionRetriever(
        base_retriever=retriever,
        base_compressor=llm_filter
    )
