from app.core.llm import get_llm
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_core.prompts import PromptTemplate

# LLMFilterChain 생성
def build_compressor():
    llm = get_llm()

    # LLMChainFilter 생성
    llm_filter = LLMChainFilter.from_llm(llm)

    return llm_filter
