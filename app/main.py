from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from . import models
from .database import engine, SessionLocal
from .routes import users, records, summary
from .middleware import LoggingMiddleware

# Create DB schemas
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    db = SessionLocal()
    try:
        admin_user = db.query(models.User).filter_by(email="admin@test.com").first()
        if not admin_user:
            admin = models.User(
                name="Admin",
                email="admin@test.com",
                role=models.RoleEnum.admin,
                status=models.StatusEnum.active
            )
            db.add(admin)
            db.commit()
            print("Default admin user created successfully.")
    finally:
        db.close()
    yield
    # Shutdown logic

app = FastAPI(
    title="Finance Data Processing and Access Control Backend",
    lifespan=lifespan
)

# Add Middleware
app.add_middleware(LoggingMiddleware)

# Custom Exception Handler to force 422 into 400 for strict bad formatted requests
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "body": exc.body},
    )

app.include_router(users.router)
app.include_router(records.router)
app.include_router(summary.router)

@app.get("/", tags=["root"], summary="API Root", description="Welcome endpoint of the Finance Dashboard API.")
def root():
    return {"message": "Welcome to the Finance Dashboard Backend. Check /docs for API documentation."}

@app.get("/health", tags=["health"], summary="Health Check", description="Returns standard application status.")
def get_health():
    return {
        "status": "ok",
        "service": "finance-backend"
    }