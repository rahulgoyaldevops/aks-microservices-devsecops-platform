import os
import time
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Orders Backend Service", version="1.0.0")

# Azure PostgreSQL Flexible Server PaaS configuration from environment variables
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", ""),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "ordersdb"),
    "user": os.getenv("POSTGRES_USER", ""),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "sslmode": os.getenv("POSTGRES_SSLMODE", "require"),
}

REQUEST_COUNT = 0
START_TIME = time.time()


@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


@app.get("/readyz")
def readyz():
    db_configured = bool(POSTGRES_CONFIG["host"] and POSTGRES_CONFIG["database"])
    return {
        "status": "ready",
        "database_configured": db_configured,
        "sslmode": POSTGRES_CONFIG["sslmode"],
    }


@app.get("/api/v1/orders")
def list_orders():
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    return {
        "orders": [
            {"id": "ord-1001", "item": "AKS Node Pool", "quantity": 3, "status": "confirmed"},
            {"id": "ord-1002", "item": "Azure PostgreSQL Flexible", "quantity": 1, "status": "provisioned"},
        ],
        "source": "azure-postgresql-flexible" if POSTGRES_CONFIG["host"] else "in-memory-fallback",
    }


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    uptime = round(time.time() - START_TIME, 2)
    return (
        f"# HELP orders_requests_total Total requests to /api/v1/orders\n"
        f"# TYPE orders_requests_total counter\n"
        f"orders_requests_total {REQUEST_COUNT}\n"
        f"# HELP service_uptime_seconds Service uptime in seconds\n"
        f"# TYPE service_uptime_seconds gauge\n"
        f"service_uptime_seconds {uptime}\n"
    )
