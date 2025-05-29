from langchain_upstage import ChatUpstage


def get_llm():
    return ChatUpstage(
        model="solar-pro",
        temperature=0  # 창의성
    )
