# from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.schemas import ExtractedCandidateData, EvaluatorOutput, CriticOutput
from app.agents.state import AgentState

# Wrapper class to show structural maturity, as requested by the roadmap


# This was for openai key
# class AzureLLMClient:
#     def __init__(self):
#         # Using standard OpenAI here for ease of execution, 
#         # but encapsulated to demonstrate production-ready patterns.
#         self.llm = ChatOpenAI(temperature=0, model=settings.model_name, api_key=settings.openai_api_key)

# This is for Azure OpenAI key
class AzureLLMClient:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            temperature=0,
            azure_deployment=settings.azure_openai_deployment_name,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key
        )

llm_client = AzureLLMClient().llm

def extract_candidate_data(state: AgentState) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical recruiter. Extract the requested information strictly from the provided resume."),
        ("user", "Resume Text:\n{resume_text}")
    ])
    chain = prompt | llm_client.with_structured_output(ExtractedCandidateData)
    result = chain.invoke({"resume_text": state["resume_text"]})
    return {"extracted_data": result}

def evaluate_match(state: AgentState) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Evaluate the candidate against the job description. Be objective. Consider previous feedback if provided: {feedback}"),
        ("user", "Job Description:\n{job_description}\n\nCandidate Data:\n{candidate_data}")
    ])
    chain = prompt | llm_client.with_structured_output(EvaluatorOutput)
    
    # Pass critic feedback if it exists from a previous loop
    critic_review = state.get("critic_review")
    feedback = critic_review.feedback if critic_review else "No previous feedback."
    
    result = chain.invoke({
        "job_description": state["job_description"],
        "candidate_data": state["extracted_data"].model_dump_json(),
        "feedback": feedback
    })
    return {"evaluation": result, "revision_count": state.get("revision_count", 0) + 1}

def critique_evaluation(state: AgentState) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a bias-checking critic. Review the evaluation for fairness and hallucinated requirements. Do not let the evaluator penalize for skills not actually in the JD."),
        ("user", "Job Description:\n{job_description}\n\nEvaluation Summary:\n{evaluation}")
    ])
    chain = prompt | llm_client.with_structured_output(CriticOutput)
    result = chain.invoke({
        "job_description": state["job_description"],
        "evaluation": state["evaluation"].model_dump_json()
    })
    return {"critic_review": result}