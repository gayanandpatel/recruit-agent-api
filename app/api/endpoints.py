from fastapi import APIRouter, HTTPException
from app.core.schemas import EvaluationRequest, FinalEvaluationResponse
from app.agents.graph import agent_executor

router = APIRouter()

@router.post("/evaluate", response_model=FinalEvaluationResponse)
async def evaluate_candidate(request: EvaluationRequest):
    try:
        # Initialize the state
        initial_state = {
            "resume_text": request.resume_text,
            "job_description": request.job_description,
            "revision_count": 0
        }
        
        # Run the LangGraph workflow
        final_state = agent_executor.invoke(initial_state)
        
        # Map the state back to our final API response schema
        return FinalEvaluationResponse(
            candidate_data=final_state["extracted_data"],
            final_score=final_state["evaluation"].score,
            missing_skills=final_state["evaluation"].missing_skills,
            evaluation_summary=final_state["evaluation"].reasoning
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))