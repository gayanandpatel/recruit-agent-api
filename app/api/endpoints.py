from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.core.schemas import FinalEvaluationResponse
from app.agents.graph import agent_executor
from app.core.parsers import extract_text_from_file

router = APIRouter()

@router.post("/evaluate", response_model=FinalEvaluationResponse)
async def evaluate_candidate(
    # Change input to accept an uploaded file and a form text field
    resume: UploadFile = File(..., description="Upload the candidate's resume (PDF, DOCX, TXT)"),
    job_description: str = Form(..., description="Paste the job description text here")
):
    try:
        # 1. Read the uploaded file into memory
        file_bytes = await resume.read()
        
        # 2. Extract text based on the file extension
        resume_text = extract_text_from_file(file_bytes, resume.filename)
        
        # 3. Initialize the LangGraph state
        initial_state = {
            "resume_text": resume_text,
            "job_description": job_description,
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
        # Catch our specific parsing errors (e.g., wrong file type)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch LLM or internal server errors
        raise HTTPException(status_code=500, detail=str(e))