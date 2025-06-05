from app.data.vector_store import load_vector_store
from app.core.compressor import build_compressor
from langchain.retrievers import ContextualCompressionRetriever


async def get_retriever():
    vector_store = await load_vector_store()

    # 벡터 저장소를 통해 retriever 생성
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return ContextualCompressionRetriever(
        base_retriever=retriever,
        base_compressor=build_compressor()
    )
