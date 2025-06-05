import os
from python.config.setting import setting
from python.infrastructure.embedding_model import get_embedding_model
from python.infrastructure.text_splitter import load_split_documents
from langchain_chroma import Chroma


async def load_vector_store():
    embedding = get_embedding_model()

    # 기존 벡터 저장소를 재사용하고, 없을 경우 새 인스턴스를 생성
    if os.path.exists(setting.CHROMA_DIR):
        return Chroma(
            embedding_function=embedding,
            collection_name="org_chart",
            persist_directory=setting.CHROMA_DIR
        )
    else:
        split_documents = await load_split_documents()

        return Chroma.from_documents(
            documents=split_documents,
            embedding=embedding,
            collection_name="org_chart",
            persist_directory=setting.CHROMA_DIR
        )
