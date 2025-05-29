from app.core.chain import chain


def search_org_chart(query: str) -> dict:
    return chain.invoke(query)
