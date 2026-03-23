from pydantic import BaseModel, Field
from typing import List

# Input Models
class EvaluationRequest(BaseModel):
    resume_text: str = Field(..., description="The raw text of the candidate's resume.")
    job_description: str = Field(..., description="The target job description.")

# Output Models from LLM Agents
class ExtractedCandidateData(BaseModel):
    skills: List[str] = Field(description="List of technical and soft skills found.")
    experience_years: int = Field(description="Total years of professional experience.")
    education: str = Field(description="Highest level of education achieved.")

class EvaluatorOutput(BaseModel):
    score: int = Field(description="Match score from 0 to 100.", ge=0, le=100)
    missing_skills: List[str] = Field(description="Skills required by JD but missing in resume.")
    reasoning: str = Field(description="Brief explanation of the score.")

class CriticOutput(BaseModel):
    is_fair: bool = Field(description="True if the evaluation is fair and unbiased, False otherwise.")
    feedback: str = Field(description="Critique of the evaluation. Empty if fair.")

# Final API Response Model
class FinalEvaluationResponse(BaseModel):
    candidate_data: ExtractedCandidateData
    final_score: int
    missing_skills: List[str]
    evaluation_summary: str