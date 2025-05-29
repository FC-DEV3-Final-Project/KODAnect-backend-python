from app.core.llm import get_llm
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import LLMChainFilter, CrossEncoderReranker, DocumentCompressorPipeline


# LLMChainFilter 결과가 없을 경우 ReRanker 실행 전 예외 방지
class SafeCompressorPipeline(DocumentCompressorPipeline):
    def compress_documents(self, documents, query, **kwargs):
        filtered = self.transformers[0].compress_documents(documents, query, **kwargs)

        if not filtered:
            return []
        reranked = self.transformers[1].compress_documents(filtered, query, **kwargs)

        return reranked


def build_compressor():
    llm = get_llm()

    # LLMChainFilter 생성
    llm_filter = LLMChainFilter.from_llm(llm)

    cross_encoder = HuggingFaceCrossEncoder(
        model_name="BAAI/bge-reranker-v2-m3"
    )
    # ReRanker 생성
    reranker = CrossEncoderReranker(
        model=cross_encoder, top_n=1
    )

    return SafeCompressorPipeline(
        transformers=[llm_filter, reranker]
    )
