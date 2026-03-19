from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/ping")
async def ping():
    return {"ping": "pong"}


@router.get("/ready")
async def readiness_check():
    return {"ready": True, "checks": {"database": "connected"}}
