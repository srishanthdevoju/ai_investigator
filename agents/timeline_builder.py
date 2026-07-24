"""
Timeline Builder Agent
Extracts chronological events from evidence using RAG and LLM.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import config


class TimelineBuilderAgent:
    """Builds a chronological timeline from collected evidence."""

    def __init__(self, llm: ChatGroq = None):
        self.llm = llm or ChatGroq(
            model=config.GROQ_MODEL,
            groq_api_key=config.GROQ_API_KEY,
            temperature=config.GROQ_TEMPERATURE,
        )

    def run(self, topic: str, evidence: str, vector_store=None) -> dict:
        """Build timeline from evidence and vector store context."""

        # RAG: retrieve additional date-related context from vector store
        rag_context = ""
        if vector_store:
            try:
                date_queries = [
                    f"timeline of {topic}",
                    f"key dates and events related to {topic}",
                    f"when did {topic} start and what happened",
                ]
                retrieved_docs = []
                for query in date_queries:
                    docs = vector_store.similarity_search(query, k=3)
                    retrieved_docs.extend(docs)

                # Deduplicate
                seen = set()
                unique_docs = []
                for doc in retrieved_docs:
                    if doc.page_content not in seen:
                        seen.add(doc.page_content)
                        unique_docs.append(doc)

                rag_context = "\n\n".join(
                    f"[{doc.metadata.get('source', 'Unknown')}]: {doc.page_content}"
                    for doc in unique_docs[:6]
                )
            except Exception:
                rag_context = ""

        # Combine evidence + RAG context
        full_context = f"{evidence}\n\nAdditional Context:\n{rag_context}" if rag_context else evidence

        # Build timeline using LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", config.TIMELINE_BUILDER_PROMPT),
        ])
        chain = prompt | self.llm | StrOutputParser()
        timeline = chain.invoke({"topic": topic, "context": full_context})

        return {
            "timeline": timeline,
            "rag_context": rag_context,
        }
