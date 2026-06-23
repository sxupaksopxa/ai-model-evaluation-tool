from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class RatingRequest(BaseModel):
    evaluation_id: str | None = None
    model_id: str = Field(..., min_length=1)
    task_id: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)
    notes: str | None = None


@router.post("/")
def create_rating(payload: RatingRequest):
    return {
        "status": "received",
        "persisted": False,
        "message": "Ratings are not stored. This application does not persist any data.",
        "rating": payload.model_dump(),
    }