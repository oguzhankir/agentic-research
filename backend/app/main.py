from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import research

app = FastAPI(
    title="Agentic Research Studio API",
    description="API for Agentic Research Studio",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(research.router, prefix="/research", tags=["research"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

