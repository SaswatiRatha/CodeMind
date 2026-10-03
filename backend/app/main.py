import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.repositories import router as repository_router
from app.config import APP_NAME, ENVIRONMENT
from app.database import Base, engine
from app.models.repository import Repository

app = FastAPI(title=APP_NAME)

Base.metadata.create_all(bind=engine)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

@app.get("/")
def root():
    return {"message": f"Welcome to {APP_NAME}"}

@app.get("/health")
def health():
    return {"status": "ok", "environment": ENVIRONMENT}

@app.get("/async_test")
async def async_test():
    await asyncio.sleep(3)

    return {
        "message": "Async operation finished"
    }

app.include_router(repository_router)

