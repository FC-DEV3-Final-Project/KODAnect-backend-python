import os
from app.config.settings import settings
from app.core.embeddings import get_embedding_model
from app.core.text_splitter import load_split_documents
from langchain_chroma import Chroma


def load_vector_store():
    embedding = get_embedding_model()

    if os.path.exists(settings.CHROMA_DIR):
        print("존재하는 벡터 저장소를 사용하겠습니다.")

        return Chroma(
            embedding_function=embedding,
            collection_name="org_chart",
            persist_directory=settings.CHROMA_DIR
        )
    else:
        print("벡터 저장소가 없어 새로 생성합니다.")
        split_documents = load_split_documents()

        return Chroma.from_documents(
            documents=split_documents,
            embedding=embedding,
            collection_name="org_chart",
            persist_directory=settings.CHROMA_DIR
        )
