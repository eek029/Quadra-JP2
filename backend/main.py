from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routers import auth, users, approvals, reservations, admin

app = FastAPI(
    title="Quadra Token API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/v1/openapi.json"
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(approvals.router, prefix="/api/v1")
app.include_router(reservations.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/healthz")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/metrics")
async def metrics():
    # TODO: Implement Prometheus metrics
    return {"status": "metrics_placeholder"}
