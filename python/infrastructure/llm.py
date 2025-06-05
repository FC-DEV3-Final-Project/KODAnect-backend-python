from functools import lru_cache
from langchain_upstage import ChatUpstage

# ==============================
# LLM 생성 함수 (싱글톤)
# ==============================
@lru_cache()
def get_llm():
    return ChatUpstage(
        model="solar-pro",
        temperature=0  # 창의성
    )
