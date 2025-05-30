from app.core.document_loader import load_org_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter


async def load_split_documents():
    documents = await load_org_documents()
    text_splitter = get_text_splitter()  # 텍스트 분할기 생성

    return text_splitter.split_documents(documents)  # 텍스트 분할기로 Document 객체를 분할하여 반환


def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        separators=["\n\n", "\n"]
    )
