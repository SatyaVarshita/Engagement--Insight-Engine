from fastapi import FastAPI, HTTPException
from app.schemas import EngagementAnalysisRequest, EngagementAnalysisResponse
from app.nudge_engine import NudgeEngine

# Initialize FastAPI app
app = FastAPI(
    title="Engagement Insight Engine",
    description="AI-based microservice for analyzing user engagement and generating nudges",
    version="1.0.0"
)

# Initialize nudge engine
nudge_engine = NudgeEngine()

@app.get("/")
async def root():
    """Root endpoint for browser access."""
    return {"message": "Welcome to the Engagement Insight Engine API. Go to /docs for Swagger UI."}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/version")
async def version():
    """Version endpoint."""
    return {"version": "1.0.0"}

@app.post("/analyze-engagement", response_model=EngagementAnalysisResponse)
async def analyze_engagement(request: EngagementAnalysisRequest):
    """Analyze user engagement and generate nudges."""
    try:
        # Generate nudges
        nudges = nudge_engine.generate_nudges(request)
        
        # Create response
        response = EngagementAnalysisResponse(
            user_id=request.user_id,
            nudges=nudges,
            status="generated"
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating nudges: {str(e)}")