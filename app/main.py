# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.routers import health

# Main application
app = FastAPI(
    title="Async LLM Gateway",
    lifespan=lifespan # Executes the function when the app is started and when it is stopped
)


@app.get('/')
async def root():
    return {'status':'ok'}

app.inlcude(health.router)