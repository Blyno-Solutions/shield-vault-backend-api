from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health

app = FastAPI(
    title="Shield Vault API",
    description="Enterprise-Grade Zero-Trust Secure File Vault Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "Shield Vault API is running securely 🔐"}