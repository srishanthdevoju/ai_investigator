"""
Reasoning Agent
Performs cause-effect chain analysis on the evidence and timeline.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import config


class ReasoningAgent:
    """Analyzes cause-effect relationships and draws conclusions."""

    def __init__(self, llm: ChatGroq = None):
        self.llm = llm or ChatGroq(
            model=config.GROQ_MODEL,
            groq_api_key=config.GROQ_API_KEY,
            temperature=config.GROQ_TEMPERATURE,
        )

    def run(self, topic: str, evidence: str, timeline: str) -> dict:
        """Perform root cause analysis."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", config.REASONING_AGENT_PROMPT),
        ])
        chain = prompt | self.llm | StrOutputParser()
        analysis = chain.invoke({
            "topic": topic,
            "evidence": evidence,
            "timeline": timeline,
        })

        return {
            "analysis": analysis,
        }
