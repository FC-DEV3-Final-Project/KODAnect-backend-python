from python.infrastructure.llm import get_llm
from python.infrastructure.retriever import get_retriever
from python.prompt.prompt_template import get_org_chart_prompt, get_query_validation_prompt
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda

llm = get_llm()

# ==============================
# 부서 검색 체인 생성 함수
# ==============================
async def get_org_chart_chain():
    retriever = await get_retriever()

    async def format_docs(question):
        docs = await retriever.ainvoke(question)

        return {
            "query": question,
            "document": "\n\n".join([doc.page_content for doc in docs])
        }

    prompt_template = get_org_chart_prompt()

    return RunnableLambda(format_docs) | prompt_template | llm | JsonOutputParser()

# ==================================
# 사용자 질의 유효성 검사 체인 생성 함수
# ==================================
def get_query_validation_chain():
    prompt_template = get_query_validation_prompt()

    return prompt_template | llm | JsonOutputParser()