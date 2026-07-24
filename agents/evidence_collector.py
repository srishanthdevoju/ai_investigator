"""
Evidence Collector Agent
Collects research findings for a topic and stores them in a lightweight vector store.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ddgs import DDGS

import config


class SimpleTextSplitter:
    """Lightweight text splitter with 0 heavy DLL dependencies."""
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents: list[Document]) -> list[Document]:
        splits = []
        for doc in documents:
            text = doc.page_content
            if len(text) <= self.chunk_size:
                splits.append(doc)
                continue
            start = 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunk_text = text[start:end]
                splits.append(Document(page_content=chunk_text, metadata=doc.metadata))
                if end == len(text):
                    break
                start += self.chunk_size - self.chunk_overlap
        return splits


class LightweightVectorStore:
    """High-performance TF-IDF Vector Store with similarity_search interface."""
    def __init__(self, documents: list[Document]):
        self.documents = documents
        self.texts = [doc.page_content for doc in documents]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        if self.texts:
            try:
                self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)
            except Exception:
                self.tfidf_matrix = None
        else:
            self.tfidf_matrix = None

    def similarity_search(self, query: str, k: int = 3) -> list[Document]:
        if self.tfidf_matrix is None or not self.texts:
            return self.documents[:k]
        try:
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            top_indices = np.argsort(scores)[::-1][:k]
            return [self.documents[i] for i in top_indices]
        except Exception:
            return self.documents[:k]


class EvidenceCollectorAgent:
    """Collects research evidence and stores in vector DB."""

    def __init__(self, llm: ChatGroq = None):
        self.llm = llm or ChatGroq(
            model=config.GROQ_MODEL,
            groq_api_key=config.GROQ_API_KEY,
            temperature=config.GROQ_TEMPERATURE,
        )
        self.text_splitter = SimpleTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
        )
        self.vector_store = None

    def _collect_evidence_documents(self, topic: str) -> list[dict]:
        """Collect live factual web search results for the given topic using DuckDuckGo."""
        findings = []
        try:
            with DDGS() as ddgs:
                search_results = list(ddgs.text(topic, max_results=6))
                for r in search_results:
                    title = r.get("title", "Web Result")
                    url = r.get("href", "#")
                    body = r.get("body", "")
                    if body:
                        findings.append({
                            "title": title,
                            "url": url,
                            "content": f"{title}: {body}",
                        })
        except Exception as e:
            print(f"Web search warning: {e}")

        # Fallback to LLM search generation if live web search yields no results
        if not findings:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a senior investigative research analyst. Given an investigation topic, "
                 "provide 6 detailed factual research findings with source names, date estimates, and specific details. "
                 "Each finding should be 2-3 sentences with concrete context."),
                ("human", "Provide detailed research findings about: {topic}\n\n"
                 "Format each finding as:\nSOURCE: [Source Name / Organization]\nCONTENT: [Detailed factual research finding]\n\n"
                 "Provide exactly 6 findings.")
            ])
            chain = prompt | self.llm | StrOutputParser()
            result = chain.invoke({"topic": topic})

            blocks = result.split("SOURCE:")
            for block in blocks[1:]:
                parts = block.split("CONTENT:")
                source = parts[0].strip() if len(parts) > 0 else "Research Document"
                content = parts[1].strip() if len(parts) > 1 else block.strip()
                findings.append({
                    "title": source,
                    "url": "#",
                    "content": content,
                })

        return findings if findings else [{"title": "LLM Research", "url": "#", "content": "No findings available."}]

    def _build_vector_store(self, results: list[dict]):
        """Build a vector store from research findings."""
        documents = []
        for r in results:
            content = r.get("content", "")
            if content:
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": r.get("title", "Unknown"),
                        "url": r.get("url", "#"),
                    },
                )
                documents.append(doc)

        if not documents:
            documents = [Document(page_content="No evidence found.", metadata={"source": "N/A"})]

        splits = self.text_splitter.split_documents(documents)
        return LightweightVectorStore(splits)

    def run(self, topic: str) -> dict:
        """Execute evidence collection."""
        search_results = self._collect_evidence_documents(topic)

        self.vector_store = self._build_vector_store(search_results)

        combined_text = "\n\n".join(
            f"[{r.get('title', 'Source')}]: {r.get('content', '')}" for r in search_results
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", config.EVIDENCE_COLLECTOR_PROMPT),
        ])
        chain = prompt | self.llm | StrOutputParser()
        evidence = chain.invoke({"topic": topic, "search_results": combined_text})

        return {
            "evidence": evidence,
            "sources": [
                {"title": r.get("title", ""), "url": r.get("url", "#")}
                for r in search_results
            ],
            "vector_store": self.vector_store,
            "raw_results": combined_text,
        }
