import os
from app.config.settings import settings
from app.core.embeddings import get_embedding_model
from app.core.text_splitter import load_split_documents
from langchain_chroma import Chroma


async def load_vector_store():
    embedding = get_embedding_model()

    # 기존 벡터 저장소를 재사용하고, 없을 경우 새 인스턴스를 생성
    if os.path.exists(settings.CHROMA_DIR):
        return Chroma(
            embedding_function=embedding,
            collection_name="org_chart",
            persist_directory=settings.CHROMA_DIR
        )
    else:
        split_documents = await load_split_documents()

        return Chroma.from_documents(
            documents=split_documents,
            embedding=embedding,
            collection_name="org_chart",
            persist_directory=settings.CHROMA_DIR
        )
