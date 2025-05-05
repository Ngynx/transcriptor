from fastapi import APIRouter
from .router import router as transcriptor_router

transcriptor_module = APIRouter(prefix="/transcriptor", tags=["Transcriptor"])
transcriptor_module.include_router(transcriptor_router)