"""
AI Investigator — Streamlit Frontend
A detective-themed autonomous investigation agent interface.
"""

import streamlit as st
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import InvestigationOrchestrator
import config

# ─── Page Config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Investigator 🔍",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Global ──────────────────────────────── */
    .stApp {
        background: linear-gradient(145deg, #0a0a0f 0%, #111827 50%, #0f172a 100%);
        font-family: 'Outfit', sans-serif;
    }

    /* ── Header ──────────────────────────────── */
    .hero-container {
        text-align: center;
        padding: 2rem 1rem 1rem;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #f59e0b 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    /* ── Agent Cards ─────────────────────────── */
    .agent-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.7), rgba(15,23,42,0.7));
        border: 1px solid rgba(245,158,11,0.15);
        border-radius: 16px;
        padding: 1.3rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(20px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .agent-card:hover {
        border-color: rgba(245,158,11,0.4);
        box-shadow: 0 0 30px rgba(245,158,11,0.08);
        transform: translateY(-2px);
    }
    .agent-card.active {
        border-color: #f59e0b;
        box-shadow: 0 0 40px rgba(245,158,11,0.15);
        animation: pulse-border 2s ease-in-out infinite;
    }
    .agent-card.done {
        border-color: #22c55e;
        box-shadow: 0 0 20px rgba(34,197,94,0.1);
    }
    @keyframes pulse-border {
        0%, 100% { box-shadow: 0 0 20px rgba(245,158,11,0.1); }
        50% { box-shadow: 0 0 40px rgba(245,158,11,0.25); }
    }
    .agent-name {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.3rem;
    }
    .agent-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #64748b;
    }
    .agent-status.running {
        color: #f59e0b;
    }
    .agent-status.complete {
        color: #22c55e;
    }

    /* ── Report Section ──────────────────────── */
    .report-container {
        background: linear-gradient(135deg, rgba(30,41,59,0.5), rgba(15,23,42,0.6));
        border: 1px solid rgba(245,158,11,0.2);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(20px);
    }
    .report-container h1, .report-container h2 {
        font-family: 'Outfit', sans-serif;
        color: #f59e0b;
    }
    .report-container h1 { font-size: 1.8rem; }
    .report-container h2 {
        font-size: 1.2rem;
        border-bottom: 1px solid rgba(245,158,11,0.2);
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }

    /* ── Sidebar ─────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(245,158,11,0.1);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #f59e0b;
        font-family: 'Outfit', sans-serif;
    }

    /* ── Case History Item ────────────────────── */
    .case-item {
        background: rgba(30,41,59,0.5);
        border: 1px solid rgba(100,116,139,0.2);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .case-item:hover {
        border-color: rgba(245,158,11,0.4);
        background: rgba(30,41,59,0.8);
    }
    .case-topic {
        color: #e2e8f0;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .case-time {
        color: #64748b;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Input Styling ───────────────────────── */
    .stTextInput > div > div > input {
        background: rgba(15,23,42,0.8) !important;
        border: 1px solid rgba(245,158,11,0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.05rem !important;
        padding: 0.8rem 1.2rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 20px rgba(245,158,11,0.15) !important;
    }

    /* ── Buttons ──────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #0f172a !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        box-shadow: 0 0 30px rgba(245,158,11,0.3) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Select box styling ──────────────────── */
    .stSelectbox > div > div {
        background: rgba(15,23,42,0.8) !important;
        border: 1px solid rgba(245,158,11,0.3) !important;
        border-radius: 10px !important;
    }

    /* ── Expanders ────────────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(30,41,59,0.5) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Metrics ──────────────────────────────── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(30,41,59,0.6), rgba(15,23,42,0.6));
        border: 1px solid rgba(245,158,11,0.15);
        border-radius: 14px;
        padding: 1rem;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #f59e0b !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Spinner ──────────────────────────────── */
    .stSpinner > div {
        border-top-color: #f59e0b !important;
    }

    /* ── Scrollbar ────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #f59e0b; }

    /* ── Hide Streamlit defaults ──────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ────────────────────────────────────────────
if "case_history" not in st.session_state:
    st.session_state.case_history = []
if "current_report" not in st.session_state:
    st.session_state.current_report = None
if "investigation_results" not in st.session_state:
    st.session_state.investigation_results = None
if "is_investigating" not in st.session_state:
    st.session_state.is_investigating = False


# ─── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🕵️ Control Panel")
    st.markdown("---")

    # Model selector
    model_name = st.selectbox(
        "🤖 AI Model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.6-27b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ],
        index=0,
        help="Select model for agent execution",
    )

    st.markdown("---")

    # Agent Pipeline Info
    st.markdown("### 🔗 Agent Pipeline")
    agents_info = [
        ("🔍", "Evidence Collector", "Web search & TF-IDF storage"),
        ("📅", "Timeline Builder", "Chronological event extraction"),
        ("🧠", "Reasoning Agent", "Cause-effect chain analysis"),
        ("📝", "Report Generator", "Structured report assembly"),
    ]
    for icon, name, desc in agents_info:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-name">{icon} {name}</div>
            <div class="agent-status">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Case History
    st.markdown("### 📁 Case History")
    if st.session_state.case_history:
        for i, case in enumerate(reversed(st.session_state.case_history)):
            if st.button(f"📋 {case['topic'][:40]}...", key=f"case_{i}", use_container_width=True):
                st.session_state.current_report = case["report"]
                st.session_state.investigation_results = case["results"]
                st.rerun()
    else:
        st.caption("No investigations yet. Start one above! ☝️")


# ─── Hero Section ──────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🕵️ AI INVESTIGATOR</div>
    <div class="hero-subtitle">Autonomous Multi-Agent Investigation System</div>
</div>
""", unsafe_allow_html=True)


# ─── Input Section ─────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "🔎 Enter investigation topic",
        placeholder="e.g. Why did Silicon Valley Bank collapse?",
        label_visibility="collapsed",
    )
with col2:
    investigate_btn = st.button("🔍 Investigate", use_container_width=True)

# Quick suggestions
st.markdown("##### 💡 Quick Cases")
suggestion_cols = st.columns(5)
suggestions = [
    "Why did Silicon Valley Bank collapse?",
    "What caused the Theranos fraud?",
    "Why did the Titanic sink?",
    "What caused the Chernobyl disaster?",
    "Why did FTX collapse?",
]
for i, suggestion in enumerate(suggestions):
    with suggestion_cols[i]:
        if st.button(suggestion[:25] + "...", key=f"sug_{i}", use_container_width=True):
            topic = suggestion
            investigate_btn = True

st.markdown("---")


# ─── Investigation Pipeline ────────────────────────────────────────
if investigate_btn and topic:
    st.session_state.is_investigating = True
    st.session_state.current_report = None
    st.session_state.investigation_results = None

    st.markdown(f"### 🕵️ Investigating: *{topic}*")

    # Metrics row
    met_col1, met_col2 = st.columns(2)
    with met_col1:
        st.metric("🤖 Model", model_name)
    with met_col2:
        st.metric("📚 Retrieval Engine", "TF-IDF Index")

    st.markdown("")

    try:
        if not config.GROQ_API_KEY:
            st.error("⚠️ GROQ_API_KEY is not set in `.env`!")
            st.session_state.is_investigating = False
            st.stop()

        orchestrator = InvestigationOrchestrator(model_name=model_name, groq_api_key=config.GROQ_API_KEY)

        # Agent Status containers
        agent_stages = [
            ("🔍 Evidence Collector Agent", "Searching the web & collecting evidence..."),
            ("📅 Timeline Builder Agent", "Extracting and ordering chronological events..."),
            ("🧠 Reasoning Agent", "Analyzing cause-effect relationships..."),
            ("📝 Report Generator Agent", "Compiling the final investigation report..."),
        ]

        results = {}

        # ── Stage 1: Evidence Collection ──
        with st.status(agent_stages[0][0], expanded=True) as status:
            st.write(agent_stages[0][1])
            start = time.time()
            evidence_result = orchestrator.evidence_agent.run(topic)
            elapsed = time.time() - start
            results["evidence"] = evidence_result["evidence"]
            results["sources"] = evidence_result["sources"]
            vector_store = evidence_result["vector_store"]
            st.write(f"✅ Collected evidence from {len(results['sources'])} sources ({elapsed:.1f}s)")
            with st.expander("📄 Raw Evidence"):
                st.markdown(results["evidence"])
            status.update(label=f"✅ {agent_stages[0][0]} — Complete", state="complete")

        # ── Stage 2: Timeline Building ──
        with st.status(agent_stages[1][0], expanded=True) as status:
            st.write(agent_stages[1][1])
            start = time.time()
            timeline_result = orchestrator.timeline_agent.run(
                topic=topic, evidence=results["evidence"], vector_store=vector_store,
            )
            elapsed = time.time() - start
            results["timeline"] = timeline_result["timeline"]
            st.write(f"✅ Timeline constructed ({elapsed:.1f}s)")
            with st.expander("📅 Timeline Events"):
                st.markdown(results["timeline"])
            status.update(label=f"✅ {agent_stages[1][0]} — Complete", state="complete")

        # ── Stage 3: Reasoning ──
        with st.status(agent_stages[2][0], expanded=True) as status:
            st.write(agent_stages[2][1])
            start = time.time()
            reasoning_result = orchestrator.reasoning_agent.run(
                topic=topic, evidence=results["evidence"], timeline=results["timeline"],
            )
            elapsed = time.time() - start
            results["analysis"] = reasoning_result["analysis"]
            st.write(f"✅ Analysis complete ({elapsed:.1f}s)")
            with st.expander("🧠 Cause-Effect Analysis"):
                st.markdown(results["analysis"])
            status.update(label=f"✅ {agent_stages[2][0]} — Complete", state="complete")

        # ── Stage 4: Report Generation ──
        with st.status(agent_stages[3][0], expanded=True) as status:
            st.write(agent_stages[3][1])
            start = time.time()
            report_result = orchestrator.report_agent.run(
                topic=topic, evidence=results["evidence"],
                timeline=results["timeline"], analysis=results["analysis"],
            )
            elapsed = time.time() - start
            results["report"] = report_result["report"]
            st.write(f"✅ Report generated ({elapsed:.1f}s)")
            status.update(label=f"✅ {agent_stages[3][0]} — Complete", state="complete")

        # Store results
        st.session_state.current_report = results["report"]
        st.session_state.investigation_results = results
        st.session_state.case_history.append({
            "topic": topic,
            "report": results["report"],
            "results": results,
        })
        st.session_state.is_investigating = False

    except Exception as e:
        st.error(f"❌ Investigation failed: {str(e)}")
        st.markdown("""
        **Troubleshooting:**
        1. Is your **Groq API Key** valid? (Get a free key at [console.groq.com](https://console.groq.com))
        2. Did you hit Groq rate limits? Try selecting another model like `openai/gpt-oss-20b`.
        3. Ensure your internet connection is active for DuckDuckGo web search.
        """)
        st.session_state.is_investigating = False


# ─── Display Report ────────────────────────────────────────────────
if st.session_state.current_report:
    st.markdown("---")
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.current_report)
    st.markdown('</div>', unsafe_allow_html=True)

    # Show sources if available
    if st.session_state.investigation_results and st.session_state.investigation_results.get("sources"):
        with st.expander("📚 Sources"):
            for src in st.session_state.investigation_results["sources"]:
                title = src.get("title", "Unknown")
                url = src.get("url", "#")
                if url and url != "#":
                    st.markdown(f"- [{title}]({url})")
                else:
                    st.markdown(f"- {title}")

    # Download button
    st.download_button(
        label="📥 Download Report",
        data=st.session_state.current_report,
        file_name="investigation_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

elif not st.session_state.is_investigating:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🕵️‍♂️</div>
        <div style="color: #64748b; font-size: 1.2rem; font-family: 'Outfit', sans-serif;">
            Enter a topic above and click <strong style="color:#f59e0b">Investigate</strong> to begin
        </div>
        <div style="color: #475569; font-size: 0.9rem; margin-top: 0.8rem; font-family: 'JetBrains Mono', monospace;">
            Four AI agents will work together to investigate your case
        </div>
    </div>
    """, unsafe_allow_html=True)
