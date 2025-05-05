from fastapi import FastAPI
from app.modules.transcripter.module import transcriptor_module

app = FastAPI()
app.include_router(transcriptor_module)

@app.get("/")
def read_root():
    return {"message": "Hello World"} 