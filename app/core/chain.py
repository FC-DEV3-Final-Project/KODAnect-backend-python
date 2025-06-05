from app.core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
from app.core.retriever import get_retriever


llm = get_llm()

async def get_org_chart_chain():
    retriever = await get_retriever()

    async def format_docs(question):
        docs = await retriever.ainvoke(question)

        return {
            "query": question,
            "document": "\n\n".join([doc.page_content for doc in docs])
        }

    prompt_template = ChatPromptTemplate.from_template(
        """
        당신은 회사 조직도 기반으로 질문을 분석하고, 적절한 부서를 찾을 뒤 부서와 전화번호를 안내하는 챗봇입니다.
    
        ## 답변
        다음 조건에 따라 JSON 형식으로 응답하세요:
        1. 관련 문서가 있는 경우:
            - dept: 관련 문서의 부서명
            - tel_no: 부서 전화번호
            - is_exist: true
        
        2. 관련 문서가 없는 경우:
            - message: "해당 질문과 관련된 정보를 찾을 수 없습니다. 다시 질문해 주세요."
            - is_exist: false
    
        ## 사용자 질문
        {query}
    
        ## 관련 문서
        {document}
        """
    )

    return RunnableLambda(format_docs) | prompt_template | llm | JsonOutputParser()

def get_query_validation_chain():
    prompt_template = ChatPromptTemplate.from_template(
    """
    당신은 질문 품질을 평가하는 AI 필터입니다.
    
    아래 기준에 따라 사용자의 질문이 유효한지 판단하고, 기준을 충족하지 않을 경우 해당 응답 메시지를 반환하십시오:
    1. 문법적으로 완전한 문장인지 확인하십시오.
    "질문이 문법적으로 불완전합니다. 다시 작성해 주세요."
    2. 질문의 의도가 명확하게 전달되는지 확인하십시오.
    "질문의 의도를 명확히 파악할 수 없습니다. 다시 작성해 주세요."
    3. 부서 정보를 응답할 수 있는 실질적인 요청 또는 정보가 포함되어 있는지 확인하십시오.
    "부서 정보를 응답할 수 있는 질문이 아닙니다. 다시 작성해 주세요."
    4. 비속어, 장난스러운 표현 등 부적절한 언어가 포함되어 있는지 확인하십시오.
    "질문에 비속어나 부적절한 언어가 포함되어 있습니다. 다시 작성해 주세요."

    ## 사용자 질문
    {query}

    ## 답변
    {{
        "is_valid": true 또는 false,
        "reason": "이유 설명"
    }}
    """
    )

    return prompt_template | llm | JsonOutputParser()