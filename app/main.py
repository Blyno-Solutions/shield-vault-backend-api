from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, file_routes

app = FastAPI(
    title="Shield Vault API",
    description="Enterprise-Grade Zero-Trust Secure File Vault Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router)
app.include_router(file_routes.router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint returning basic API status and version info.
    """
    return {
        "message": "Shield Vault API is running securely 🔐",
        "version": app.version,
        "status": "operational",
    }