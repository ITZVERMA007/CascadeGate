# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.routers import health
from app.routers import chat
# pyrefly: ignore [missing-import]
from app.core.logging_config import setup_logging

# Initializing logging
setup_logging()

# Main application
app = FastAPI(
    title="Async LLM Gateway",
    version="0.1.0",
    lifespan=lifespan, # Executes the function when the app is started and when it is stopped
    description="High performance async inference gateway with cascade routing"
)


@app.get('/')
async def root():
    return {'status':'ok'}

app.include_router(health.router)
app.include_router(chat.router)