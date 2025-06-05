from functools import lru_cache
from langchain_upstage import UpstageEmbeddings

# ==============================
# 임베딩 모델 생성 함수 (싱글톤)
# ==============================
@lru_cache()
def get_embedding_model():
    return UpstageEmbeddings(
        model="solar-embedding-1-large"
    )
