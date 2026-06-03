from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Trash Diary API")

app.include_router(auth.router)