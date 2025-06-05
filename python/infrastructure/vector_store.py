import os
from python.core.setting import setting
from python.infrastructure.embedding_model import get_embedding_model
from python.infrastructure.text_splitter import get_split_documents
from langchain_chroma import Chroma

# ==============================
# 벡터 저장소 생성 함수
# ==============================
async def get_vector_store():
    embedding = get_embedding_model()

    # 기존 벡터 저장소를 재사용
    if os.path.exists(setting.CHROMA_DIR):
        return Chroma(
            embedding_function=embedding,
            collection_name="org_chart",
            persist_directory=setting.CHROMA_DIR
        )
    # 신규 벡터 저장소 생성
    else:
        split_documents = await get_split_documents()

        return Chroma.from_documents(
            documents=split_documents,
            embedding=embedding,
            collection_name="org_chart",
            persist_directory=setting.CHROMA_DIR
        )
