from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="RecruitAgent API",
    description="An Agentic Candidate Screening API built with FastAPI and LangGraph",
    version="1.0.0"
)

# Include the evaluation routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}