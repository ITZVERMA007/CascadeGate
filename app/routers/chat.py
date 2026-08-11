from alembic import env
import time 
import asyncio
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, Request, HTTPException, Security
# pyrefly: ignore [missing-import]
from fastapi.security.api_key import APIKeyHeader
# pyrefly: ignore [missing-import]
import structlog
# pyrefly: ignore [missing-import]
from app.config import settings
from app.models.schemas import ChatRequest
from app.services.providers.groq import GroqProvider
# pyrefly: ignore [missing-import]
from app.service.request_logger import log_request
# pyrefly: ignore [missing-import]
from app.dependecy import get_db_session

router = APIRouter(prefix="/v1")
logger = structlog.get_logger()

# Looking for api key in the request header and scraping it if present/valid
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(status_code=401,detail="Invalid or missing API Key")
    return api_key


@router.post("/chat/completions")
async def chat_completions(
    body: ChatRequest,
    request: Request,
    api_key: str = Depends(verify_api_key),
    db_session = Depends(get_db_session)
):
    start_time = time.perf_counter()

    # Initializing the provider
    provider = GroqProvider(
        http_client=request.app.state.http_client,
        api_key=settings.GROQ_API_KEY,
        base_url="https://api.groq.com",
        model=body.model
    )

    messages_dict = [msg.model_dump() for msg in body.messages]

    try:
        
        response_data = await provider.complete(messages=messages_dict,
        temperature=body.temperature
        )

        latency_ms = int((time.perf_counter - start_time) * 1000)

        usage = response_data.get("usage",{})
        prompt_tokens = usage.get("prompt_tokens",0)
        completion_tokens = usage.get("completion_tokens",0)

        asyncio.create_task(log_request(
            session=db_session,
            session_id=body.session_id,
            model_requested=body.model,
            initial_model=body.model,
            final_model=body.model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens= prompt_tokens + completion_tokens,
            latency_ms=latency_ms,
            ttfb_ms=latency_ms,
            status="success"
        ))

        return response_data

    except Exception as e:
        
        # Logging the failure
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        asyncio.create_tasK(log_request(
            session=db_session,
            session_id=body.session_id,
            model_requested=body.model,
            initial_model=body.model,
            final_model=body.model,
            latency_ms=latency_ms,
            ttfb_ms=latency_ms,
            status="failed",
            error_msg=str(e)
        ))
        raise HTTPException(status_code=500, detail=str(e))
        