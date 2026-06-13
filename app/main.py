from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.v1.appointments import router as appointments_router
from app.api.v1.users import router as users_router
from app.core import db
from app.users.errors import RepositoryError, UserAlreadyExists, UserNotFound

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


@app.exception_handler(UserAlreadyExists)
def handle_user_exists(request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=409, content={"error": "user_already_exists", "message": str(exc)}
    )


@app.exception_handler(UserNotFound)
def handle_user_not_found(request, exc: UserNotFound):
    return JSONResponse(
        status_code=404, content={"error": "user_not_found", "message": str(exc)}
    )


@app.exception_handler(RepositoryError)
def handle_repo_error(request, exc: RepositoryError):
    return JSONResponse(
        status_code=500, content={"error": "repository_error", "message": str(exc)}
    )


# Mount canonical router namespace for versioned API
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(
    appointments_router, prefix="/api/v1/appointments", tags=["appointments"]
)


# Keep `/users` as a lightweight redirect to the canonical, versioned API
# Hide these helper redirect routes from the OpenAPI schema (docs)
@app.api_route(
    "/users", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], include_in_schema=False
)
def users_redirect():
    return RedirectResponse(url="/api/v1/users")


@app.api_route(
    "/users/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    include_in_schema=False,
)
def users_redirect_with_path(full_path: str):
    return RedirectResponse(url=f"/api/v1/users/{full_path}")


# Provide shorthand redirects for appointments as well
@app.api_route(
    "/appointments",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    include_in_schema=False,
)
def appointments_redirect():
    return RedirectResponse(url="/api/v1/appointments")


@app.api_route(
    "/appointments/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    include_in_schema=False,
)
def appointments_redirect_with_path(full_path: str):
    return RedirectResponse(url=f"/api/v1/appointments/{full_path}")


@app.get("/", include_in_schema=False)
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
