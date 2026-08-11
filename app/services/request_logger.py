# pyrefly: ignore [missing-import]
import structlog
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import AsyncSession
# pyrefly: ignore [missing-import]
from app.model.tables import RequestLog

logger = structlog.get_logger()

async def log_request(session: AsyncSession, **kwargs):

    try:
        log_entry = RequestLog(**kwargs)
        session.add(log_entry)
        await session.commit()
        logger.info("request_logged_succesfully", session_id=kwargs.get("session_id"))
    except Exception as e:
        logger.error("background_log_failed", error=str(e))