# 🤖 RecruitAgent API: Agentic Candidate Screening Pipeline

[cite_start]RecruitAgent is an Agentic AI screening API built with FastAPI and LangGraph, designed to simulate an intelligent recruitment SaaS feature. [cite: 59] It automates the resume screening process by extracting data from raw documents (PDF, DOCX, TXT) and evaluating it against a job description using a self-correcting AI workflow.

---

## 📖 Overview

[cite_start]Traditional single-prompt LLM chains suffer from hallucination, so this project implemented an "Evaluator-Critic" loop using LangGraph to ensure higher reliability in candidate scoring. [cite: 60] 

Instead of relying on a single zero-shot evaluation, the system utilizes specialized AI agents to extract structured data, score the candidate objectively, and self-critique the results to eliminate bias before returning a deterministic JSON response to the client.

## 🏗️ Architecture & Flow (The Agentic Graph)

This project utilizes a stateful graph architecture to manage the LLM reasoning process:

1. [cite_start]**Extraction Node:** Takes a raw text resume and uses an LLM purely to extract structured data (Skills, Experience Years, Education) into a Pydantic model. [cite: 14]
2. [cite_start]**Evaluation Node:** Takes the extracted structured data and the Job Description. [cite: 15] It outputs a base score and identifies skill gaps.
3. [cite_start]**Critic Node (Self-Reflection):** Reviews the Evaluator's score. [cite: 17] [cite_start]If the Critic finds the score is biased or missed something in the context, it loops back to the Evaluator for a revision. [cite: 18]
4. **FastAPI Layer:** Handles asynchronous `multipart/form-data` file uploads, parses the documents into text, and serves the final structured JSON output.

## 💻 Tech Stack

* [cite_start]**Language:** Python 3.11/3.12 [cite: 7]
* [cite_start]**Web Framework:** FastAPI (essential for modern Python backends). [cite: 8]
* [cite_start]**AI Orchestration:** LangGraph (Microsoft/industry standard for building stateful, multi-actor LLM applications). [cite: 9]
* [cite_start]**Data Validation:** Pydantic V2 (Enforcing strict JSON schemas for the AI outputs). [cite: 10]
* [cite_start]**LLM Provider:** Azure OpenAI. [cite: 11]
* **Document Parsing:** `pypdf`, `python-docx`

---

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
│       ├── parsers.py           # Document extraction logic (PDF, DOCX, TXT)
│       └── schemas.py           # Pydantic models for strict LLM outputs
│
├── infrastructure/
│   └── azure_ml_finetune_job.py # Mock script demonstrating Azure ML knowledge
│
├── data/
│   ├── sample_resume_1.pdf      # Sample files for local testing
│   ├── sample_resume_2.docx
│   └── job_description.txt      
│
├── .env.example                 # Template for required API keys
├── .gitignore
├── requirements.txt
└── README.md                    # Project documentation