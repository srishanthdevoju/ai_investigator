"""
AI Investigator - Configuration
Central configuration for models, API keys, and agent prompts.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── LLM Configuration (Groq API) ──────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_TEMPERATURE = 0.3

# ─── Embedding Configuration ───────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ─── FAISS Configuration ───────────────────────────────────────────
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ─── Agent Prompts ──────────────────────────────────────────────────

EVIDENCE_COLLECTOR_PROMPT = """You are an Evidence Collector Agent — a meticulous investigator.
Given the following search results about a topic, extract the KEY pieces of evidence.

Topic: {topic}

Search Results:
{search_results}

Extract exactly 5-8 bullet points of critical evidence. Each bullet should be a concise,
factual statement with the source noted. Format as:
• [Evidence statement] (Source: [source name])

Return ONLY the bullet points, nothing else."""

TIMELINE_BUILDER_PROMPT = """You are a Timeline Builder Agent — a chronological analyst.
Given the evidence and context about a topic, construct a precise timeline of key events.

Topic: {topic}

Evidence & Context:
{context}

Build a timeline of 5-8 key events. Format EXACTLY as:
[DATE] → [Event description]

Use specific dates where possible (e.g., "Mar 8, 2023"), or approximate periods
(e.g., "Early 2022", "Q3 2021"). Order chronologically from earliest to latest.

Return ONLY the timeline entries, nothing else."""

REASONING_AGENT_PROMPT = """You are a Reasoning Agent — a cause-effect analyst and critical thinker.
Given the evidence and timeline of events, perform a root cause analysis.

Topic: {topic}

Evidence:
{evidence}

Timeline:
{timeline}

Analyze the cause-effect relationships and provide:

PRIMARY CAUSE:
[One sentence identifying the root cause]

CONTRIBUTING FACTORS:
• [Factor 1]
• [Factor 2]
• [Factor 3]
(list 3-5 contributing factors)

CAUSE-EFFECT CHAIN:
[Describe the chain of events showing how causes led to the final outcome, in 2-3 sentences]

CONCLUSION:
[A 2-3 sentence definitive conclusion summarizing your analysis]

Use the exact headers shown above."""

REPORT_GENERATOR_PROMPT = """You are a Report Generator Agent — a professional investigative report writer.
Compile all investigation findings into a polished, structured investigation report.

Topic: {topic}

Evidence Collected:
{evidence}

Timeline of Events:
{timeline}

Analysis & Reasoning:
{analysis}

Generate a professional investigation report with these EXACT sections:

# 🔍 INVESTIGATION REPORT

## 📋 Case Summary
[2-3 sentence overview of what was investigated and the key finding]

## 🔎 Evidence
[List all evidence as bullet points]

## 📅 Timeline of Events
[List all timeline events]

## 🧠 Analysis
[The cause-effect analysis and reasoning]

## ⚖️ Conclusion
[Final definitive conclusion with primary cause and recommendation if applicable]

## 📊 Confidence Level
[Rate as HIGH / MEDIUM / LOW with 1-sentence justification]

Make the report professional, clear, and well-structured."""
