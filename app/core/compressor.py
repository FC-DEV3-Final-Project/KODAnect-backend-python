from app.core.llm import get_llm
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_core.prompts import PromptTemplate


def build_compressor():
    llm = get_llm()
    # 사용자 정의 프롬프트 작성
    llm_filter_prompt = PromptTemplate.from_template(
        """
        이 문서가 쿼리에서 요청한 명확한 의도와 실제로 관련 있는 문서인지 판단하세요.
        단순 키워드 유사성만으로 판단하지 마세요. 실제로 쿼리를 만족하는 문서면 'YES', 아니면 'NO'로만 답하세요.
        
        쿼리: {query}
        문서: {document}
        """
    )

    # LLMChainFilter 생성
    llm_filter = LLMChainFilter.from_llm(llm)

    return llm_filter
