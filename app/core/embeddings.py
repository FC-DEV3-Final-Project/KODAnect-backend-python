from langchain_upstage import UpstageEmbeddings


def get_embedding_model():
    return UpstageEmbeddings(
        model="solar-embedding-1-large"
    )
