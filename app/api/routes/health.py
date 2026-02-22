from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "shield-vault-api",
        "version": "1.0.0",
    }