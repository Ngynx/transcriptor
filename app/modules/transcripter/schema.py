from pydantic import BaseModel

class TranscriptionRequest(BaseModel):
    filename: str
    model_name: str