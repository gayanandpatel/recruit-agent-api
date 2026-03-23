# 🤖 RecruitAgent API: Agentic Candidate Screening Pipeline

An asynchronous, multi-agent evaluation API built with **FastAPI** and **LangGraph**, designed to automate and standardize the resume screening process for the recruitment industry.

---

## 📖 Overview

Traditional LLM wrappers rely on zero-shot prompts, which are prone to hallucination and bias when evaluating candidates. RecruitAgent solves this by implementing an **Agentic Workflow** (Evaluator-Critic model). 

The system utilizes specialized AI agents to extract structured data from resumes, score the candidate against a specific Job Description, and self-critique the results to ensure fairness and accuracy before returning a deterministic JSON response to the client.

## 🏗️ Architecture & Flow

This project utilizes a stateful graph architecture to manage the LLM reasoning process:

1. **Extraction Node:** Parses unstructured resume text into strict Pydantic data schemas.
2. **Evaluation Node:** Compares candidate skills against the target Job Description, outputting a base score and identified skill gaps.
3. **Critic Node (Self-Reflection):** Reviews the Evaluator's output for bias or missed context. If the critique fails, the graph loops back to the Evaluator for a revised score.
4. **FastAPI Layer:** Handles asynchronous HTTP requests and serves the final structured output.

## 💻 Tech Stack

* **Backend Framework:** Python 3.11+, FastAPI, Uvicorn
* **AI Orchestration:** LangChain, LangGraph
* **Data Validation:** Pydantic V2
* **LLM Provider:** Azure OpenAI / OpenAI (Configurable)

## 📂 Project Structure

<details>
<summary><b>Click to expand the directory tree</b></summary>

```text
recruit-agent-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application instantiation
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py         # POST /api/v1/evaluate route
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py             # LangGraph TypedDict for state management
│   │   ├── nodes.py             # LLM functions (Extractor, Evaluator, Critic)
│   │   └── graph.py             # LangGraph compilation
│   └── core/
│       ├── __init__.py
│       ├── config.py            # Pydantic BaseSettings for env vars
│       └── schemas.py           # Pydantic models for strict LLM outputs
│
├── infrastructure/
│   └── azure_ml_finetune.py     # Mock script demonstrating Azure ML knowledge
│
├── data/
│   ├── sample_resume_1.txt      # Dummy data for local testing
│   ├── sample_resume_2.txt
│   └── job_description.txt      
│
├── .env.example                 # Template for required API keys
├── .gitignore
├── requirements.txt
└── README.md                    # Project documentation (You are here)
```