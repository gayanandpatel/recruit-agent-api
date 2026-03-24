from fastapi import APIRouter, HTTPException, UploadFile, File
from app.core.schemas import FinalEvaluationResponse
from app.agents.graph import agent_executor
from app.core.parsers import extract_text_from_file

router = APIRouter()

@router.post("/evaluate", response_model=FinalEvaluationResponse)
async def evaluate_candidate(
    # Both inputs are now strict file uploads
    resume: UploadFile = File(..., description="Upload the candidate's resume (PDF, DOCX, TXT)"),
    job_description: UploadFile = File(..., description="Upload the job description (PDF, DOCX, TXT)")
):
    try:
        # 1. Read both uploaded files into memory asynchronously
        resume_bytes = await resume.read()
        jd_bytes = await job_description.read()
        
        # 2. Extract text from both files using our parser utility
        resume_text = extract_text_from_file(resume_bytes, resume.filename)
        jd_text = extract_text_from_file(jd_bytes, job_description.filename)
        
        # 3. Initialize the LangGraph state with the extracted text
        initial_state = {
            "resume_text": resume_text,
            "job_description": jd_text,
            "revision_count": 0
        }
        
        # 4. Run the multi-agent workflow
        final_state = agent_executor.invoke(initial_state)
        
        # 5. Map the state back to our final API response schema
        return FinalEvaluationResponse(
            candidate_data=final_state["extracted_data"],
            final_score=final_state["evaluation"].score,
            missing_skills=final_state["evaluation"].missing_skills,
            evaluation_summary=final_state["evaluation"].reasoning
        )
        
    except ValueError as ve:
        # Catch our specific parsing errors (e.g., wrong file type uploaded)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch LLM or internal server errors
        raise HTTPException(status_code=500, detail=str(e))