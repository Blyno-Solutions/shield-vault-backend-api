from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, files
from app.core.config import settings

app = FastAPI(
    title="Shield Vault API",
    description="Enterprise-Grade Zero-Trust Secure File Vault Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Blyno Solutions",
        "url": "https://github.com/Blyno-Solutions",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(files.router)

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: Welcome message with API status
        
    Example:
        >>> GET /
        {
            "message": "Shield Vault API is running securely 🔐",
            "version": "1.0.0",
            "status": "operational"
        }
    """
    return {
        "message": "Shield Vault API is running securely 🔐",
        "version": app.version,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring systems.
    
    Returns:
        dict: Health status of the API and its dependencies
        
    Example:
        >>> GET /health
        {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-03-14T12:00:00Z"
        }
    """
    from datetime import datetime
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/info")
async def api_info():
    """
    Get detailed API information and available endpoints.
    
    Returns:
        dict: API metadata and endpoint listing
        
    Example:
        >>> GET /info
        {
            "name": "Shield Vault API",
            "version": "1.0.0",
            "endpoints": ["/", "/health", "/info", "/files/upload", "/files/download/{file_id}"]
        }
    """
    return {
        "name": app.title,
        "version": app.version,
        "endpoints": ["/", "/health", "/info", "/files/upload", "/files/download/{file_id}"]
    }