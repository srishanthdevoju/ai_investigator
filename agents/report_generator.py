"""
Report Generator Agent
Assembles all investigation findings into a polished investigation report.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import config


class ReportGeneratorAgent:
    """Generates a structured investigation report from all findings."""

    def __init__(self, llm: ChatGroq = None):
        self.llm = llm or ChatGroq(
            model=config.GROQ_MODEL,
            groq_api_key=config.GROQ_API_KEY,
            temperature=config.GROQ_TEMPERATURE,
        )

    def run(self, topic: str, evidence: str, timeline: str, analysis: str) -> dict:
        """Generate the final investigation report."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", config.REPORT_GENERATOR_PROMPT),
        ])
        chain = prompt | self.llm | StrOutputParser()
        report = chain.invoke({
            "topic": topic,
            "evidence": evidence,
            "timeline": timeline,
            "analysis": analysis,
        })

        return {
            "report": report,
        }
