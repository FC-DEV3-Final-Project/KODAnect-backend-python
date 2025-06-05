from python.infrastructure.document_loader import get_org_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==============================
# 문서 분할 함수
# ==============================
async def get_split_documents():
    documents = await get_org_documents()
    text_splitter = get_text_splitter()

    return text_splitter.split_documents(documents)

# ==============================
# 텍스트 분할기 생성 함수
# ==============================
def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        separators=["\n\n", "\n"]
    )
