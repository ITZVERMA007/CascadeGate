# pyrefly: ignore [missing-import]
import structlog
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
# pyrefly: ignore [missing-import]
from app.models.tables import RequestLog

logger = structlog.get_logger()

async def log_request(session_factory: async_sessionmaker[AsyncSession], **kwargs):

    try:
        async with session_factory() as session:
            log_entry = RequestLog(**kwargs)
            session.add(log_entry)
            await session.commit()
            logger.info("request_logged_succesfully", session_id=kwargs.get("session_id"))
    except Exception as e:
        logger.error("background_log_failed", error=str(e))