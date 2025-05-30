from app.core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
from app.core.retriever import get_retriever


async def get_chain():
    llm = get_llm()
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

