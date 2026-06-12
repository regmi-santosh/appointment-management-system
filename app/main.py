from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pathlib import Path
from .users import router as users_router
from .api import users as api_users
from . import db

# Load OpenAPI description from file when available so the API docs are richer
desc_path = Path(__file__).parent / "openapi_description.md"
if desc_path.exists():
    description = desc_path.read_text(encoding="utf-8")
else:
    description = "Backend API for appointment management (FastAPI)."

app = FastAPI(
    title="Appointment Management System",
    version="0.1.0",
    description=description,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


app.include_router(users_router, prefix="/users", tags=["users"])
# also mount canonical router namespace for future versioning
app.include_router(api_users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def read_root():
    # redirect root to API docs by default so the OpenAPI UI is the primary entrypoint
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    # initialize DB on startup
    db.init_db()
