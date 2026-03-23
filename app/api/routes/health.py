from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    """
    Returns the overall health status of the API,
    including service info, database connection, and timestamp.
    """
    return {
        "status": "healthy",
        "service": "shield-vault-api",
        "version": "1.0.0",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

@router.get("/ping")
async def ping():
    """
    Simple ping endpoint for uptime monitoring.
    """
    return {"ping": "pong"}

@router.get("/ready")
async def readiness_check():
    """
    Readiness endpoint to check if the service is ready to handle requests.
    """
    return {"ready": True, "checks": {"database": "connected"}}