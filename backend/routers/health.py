import time
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Comprehensive health check endpoint for monitoring and container orchestration.

    Checks:
        - Application status
        - Database connectivity

    Returns:
        200 OK if all checks pass
        503 Service Unavailable if any check fails
    """
    start_time = time.time()
    checks = {}
    is_healthy = True

    # Database connectivity check
    try:
        db_start = time.time()
        await db.execute(text("SELECT 1"))
        checks["database"] = {
            "status": "up",
            "latency_ms": round((time.time() - db_start) * 1000, 2),
        }
    except Exception as e:
        is_healthy = False
        checks["database"] = {
            "status": "down",
            "error": str(e),
        }

    response_time_ms = round((time.time() - start_time) * 1000, 2)

    response_body = {
        "status": "healthy" if is_healthy else "unhealthy",
        "service": settings.PROJECT_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "response_time_ms": response_time_ms,
        "checks": checks,
    }

    status_code = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(content=response_body, status_code=status_code)


@router.get("/health/live", tags=["Health"])
async def liveness_check():
    """
    Liveness probe for container orchestrators (e.g., Kubernetes).

    Returns 200 OK if the application process is running.
    Does not check external dependencies.
    """
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
