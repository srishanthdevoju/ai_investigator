# 🕵️ AI Investigator

An autonomous multi-agent investigation system. Given an investigation topic, four specialized AI agents collaborate using live web search, timeline synthesis, and root-cause reasoning to compile a structured investigation report.

## 🔗 Agent Pipeline

| Agent | Role |
|---|---|
| 🔍 **Evidence Collector** | Live DuckDuckGo web search & TF-IDF indexing |
| 📅 **Timeline Builder** | Chronological event extraction & RAG context matching |
| 🧠 **Reasoning Agent** | Cause-effect chain & root cause analysis |
| 📝 **Report Generator** | Structured markdown report compilation |

## 🛠️ Tech Stack

- **LLM**: GPT-OSS 120B / 20B, Qwen 3.6 27B via **Groq API**
- **Web Search**: DuckDuckGo (`ddgs`)
- **Agent Framework**: LangChain
- **Vector Search**: TF-IDF Similarity Index
- **Frontend**: Streamlit

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Run Application
```bash
streamlit run app.py
```

## 📁 Project Structure

```
ai_investigator/
├── app.py                     # Streamlit frontend
├── config.py                  # Configuration & system prompts
├── orchestrator.py            # Multi-agent orchestrator
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
└── agents/
    ├── evidence_collector.py  # Live web search & TF-IDF retriever agent
    ├── timeline_builder.py    # Timeline extraction agent
    ├── reasoning_agent.py     # Cause-effect analysis agent
    └── report_generator.py    # Report assembly agent
```
