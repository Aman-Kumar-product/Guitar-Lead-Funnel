from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging

# Import routes
from backend.api.routes import lead_routes

# Load environment variables from .env file
load_dotenv(override=True)

from backend.api.limiter import limiter

app = FastAPI(
    title="Guitar Lead Funnel API",
    description="Backend API for the Guitar Lead Funnel MVP",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."},
    )

# Configure CORS so the Antigravity frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP/Development; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(lead_routes.router, prefix="/api")
from backend.api.routes import booking_routes
app.include_router(booking_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Guitar Lead Funnel API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    return {"detail": "Not Found", "vercel_path_seen": request.url.path, "raw_path": request.scope.get("raw_path", b"").decode("utf-8")}
