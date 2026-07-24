"""
Investigation Orchestrator
Runs all four agents sequentially with progress callbacks.
"""

from langchain_groq import ChatGroq
from agents.evidence_collector import EvidenceCollectorAgent
from agents.timeline_builder import TimelineBuilderAgent
from agents.reasoning_agent import ReasoningAgent
from agents.report_generator import ReportGeneratorAgent
import config


class InvestigationOrchestrator:
    """Orchestrates the full investigation pipeline across all agents."""

    STAGES = [
        ("🔍 Evidence Collector", "Searching & collecting evidence..."),
        ("📅 Timeline Builder", "Building chronological timeline..."),
        ("🧠 Reasoning Agent", "Analyzing cause-effect relationships..."),
        ("📝 Report Generator", "Compiling investigation report..."),
    ]

    def __init__(self, model_name: str = None, groq_api_key: str = None):
        self.model_name = model_name or config.GROQ_MODEL
        self.groq_api_key = groq_api_key or config.GROQ_API_KEY
        self.llm = ChatGroq(
            model=self.model_name,
            groq_api_key=self.groq_api_key,
            temperature=config.GROQ_TEMPERATURE,
        )
        self.evidence_agent = EvidenceCollectorAgent(self.llm)
        self.timeline_agent = TimelineBuilderAgent(self.llm)
        self.reasoning_agent = ReasoningAgent(self.llm)
        self.report_agent = ReportGeneratorAgent(self.llm)

    def investigate(self, topic: str, progress_callback=None) -> dict:
        """
        Run the full investigation pipeline.

        Args:
            topic: The investigation topic/question
            progress_callback: Optional callable(stage_index, stage_name, status, result)

        Returns:
            Dict with all agent outputs and final report
        """
        results = {}

        def update(stage_idx, result=None):
            if progress_callback:
                name, status = self.STAGES[stage_idx]
                progress_callback(stage_idx, name, status, result)

        # ── Stage 1: Evidence Collection ──────────────────────────
        update(0)
        evidence_result = self.evidence_agent.run(topic)
        results["evidence"] = evidence_result["evidence"]
        results["sources"] = evidence_result["sources"]
        vector_store = evidence_result["vector_store"]
        update(0, evidence_result)

        # ── Stage 2: Timeline Building ────────────────────────────
        update(1)
        timeline_result = self.timeline_agent.run(
            topic=topic,
            evidence=results["evidence"],
            vector_store=vector_store,
        )
        results["timeline"] = timeline_result["timeline"]
        update(1, timeline_result)

        # ── Stage 3: Reasoning & Analysis ─────────────────────────
        update(2)
        reasoning_result = self.reasoning_agent.run(
            topic=topic,
            evidence=results["evidence"],
            timeline=results["timeline"],
        )
        results["analysis"] = reasoning_result["analysis"]
        update(2, reasoning_result)

        # ── Stage 4: Report Generation ────────────────────────────
        update(3)
        report_result = self.report_agent.run(
            topic=topic,
            evidence=results["evidence"],
            timeline=results["timeline"],
            analysis=results["analysis"],
        )
        results["report"] = report_result["report"]
        update(3, report_result)

        return results
