from fastapi import APIRouter
from .schema import TranscriptionRequest
from .service import transcribe_audio

router = APIRouter()


@router.post("/")
def transcribe(req: TranscriptionRequest):
    return transcribe_audio(req.filename, req.model_name)