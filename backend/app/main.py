from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from slowapi.errors import RateLimitExceeded
import logging
import os

from app.limiter import limiter
from app.modules.tasks.routes import router as tasks_router
from app.modules.models.routes import router as models_router
from app.modules.evaluations.routes import router as evaluations_router
from app.modules.ratings.routes import router as ratings_router
from app.modules.statistics.routes import router as statistics_router

app = FastAPI(
    title="AI Model Evaluation Tool API",
    description="Backend API for comparing AI models on practical business tasks.",
    version="0.1.0",
)

load_dotenv()

logger = logging.getLogger(__name__)

# Rate limiting: 10 requests per minute per IP
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please slow down."},
    )

# CORS: allow comma-separated origins from env, fallback to localhost
_allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5174")
allow_origins = [o.strip() for o in _allowed_origins.split(",") if o.strip()]

# Reject wildcard origins when credentials are enabled
if any("*" in o for o in allow_origins):
    logger.warning("ALLOWED_ORIGINS contains wildcard '*' with allow_credentials=True; filtering wildcards")
    allow_origins = [o for o in allow_origins if "*" not in o]
    if not allow_origins:
        allow_origins = ["http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self' https:; "
        "frame-ancestors 'none';"
    )
    return response

# Request body size limit: 10 MB
@app.middleware("http")
async def limit_request_size(request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10 * 1024 * 1024:
        return JSONResponse(
            status_code=413,
            content={"detail": "Request body too large (max 10MB)"},
        )
    return await call_next(request)

# HTTPS redirect in production (skip localhost)
@app.middleware("http")
async def https_redirect(request, call_next):
    host = request.headers.get("host", "")
    if "localhost" in host or "127.0.0.1" in host:
        return await call_next(request)
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    if proto == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(str(url), status_code=301)
    return await call_next(request)

@app.get("/")
def root():
    return {
        "app": "AI Model Evaluation Tool API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# API routes
app.include_router(tasks_router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(models_router, prefix="/api/models", tags=["Models"])
app.include_router(evaluations_router, prefix="/api/evaluations", tags=["Evaluations"])
app.include_router(ratings_router, prefix="/api/ratings", tags=["Ratings"])
app.include_router(statistics_router, prefix="/api/statistics", tags=["Statistics"])