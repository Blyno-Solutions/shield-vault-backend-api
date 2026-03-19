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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(file_routes.router)


@app.get("/")
async def root():
    return {
        "message": "Shield Vault API is running securely 🔐",
        "version": app.version,
        "status": "operational",
    }
