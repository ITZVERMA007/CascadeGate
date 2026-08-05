import time
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Request,status
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
# pyrefly: ignore [missing-import]
from sqlalchemy import text

router = APIRouter(tags=["Health"])
@router.get("/health")
async def health_check(request: Request):

    # Ping database and redis to check if they are operational or not

    redis_status = "down"
    db_status = "down"
    is_healthy = True

    try:
        await request.app.state.redis.ping()
        redis_status = "connected"

    except Exception:
        is_healthy = False
    
    try:
        async with request.app.state.db_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        is_healthy = False
    
    up_time = time.time() - request.app.state.startup_time

    response_data = {
        "status":"healthy" if is_healthy else "not_healthy",
        "redis": redis_status,
        "postgres": db_status,
        "up_time": round(up_time,2)
    }

    # Status code according to the health of the components
    status_code = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(status_code=status_code,content=response_data)