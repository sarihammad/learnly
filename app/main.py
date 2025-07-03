from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Learnly: AI-Powered Learning Paths")
app.include_router(router)