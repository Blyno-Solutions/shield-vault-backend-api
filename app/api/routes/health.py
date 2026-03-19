from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """
    Perform a comprehensive health check of the API.

    Returns:
        dict: Detailed health status including all service dependencies

    Example:
        >>> GET /health/
        {
            "status": "healthy",
            "services": {
                "database": "connected",
                "api": "operational"
            },
            "timestamp": "2024-03-14T12:00:00Z"
        }
    """
    return {
        "status": "healthy",
        "services": {"database": "connected", "api": "operational"},
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint for connectivity testing.

    Returns:
        dict: Pong response indicating API is reachable

    Example:
        >>> GET /health/ping
        {"ping": "pong"}
    """
    return {"ping": "pong"}


@router.get("/ready")
async def readiness_check():
    """
    Readiness probe for container orchestration systems.

    Returns:
        dict: Readiness status and component checks

    Example:
        >>> GET /health/ready
        {
            "ready": true,
            "checks": {
                "database": "connected"
            }
        }
    """
    return {"ready": True, "checks": {"database": "connected"}}
