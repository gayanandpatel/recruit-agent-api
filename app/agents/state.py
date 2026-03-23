from typing import TypedDict, Optional
from app.core.schemas import ExtractedCandidateData, EvaluatorOutput, CriticOutput

class AgentState(TypedDict):
    resume_text: str
    job_description: str
    extracted_data: Optional[ExtractedCandidateData]
    evaluation: Optional[EvaluatorOutput]
    critic_review: Optional[CriticOutput]
    revision_count: int