from fastapi import APIRouter
from app.schemas import CurriculumRequest
from app.services.generator import generate_learning_path

router = APIRouter()

@router.post("/generate")
def generate(request: CurriculumRequest):
    """
    API endpoint to generate a personalized learning path.

    Args:
        request (CurriculumRequest): Input JSON with 'goal' and optional 'known_skills'.

    Returns:
        dict: Structured learning path or error details.
    """
    return generate_learning_path(request)