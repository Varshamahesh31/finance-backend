from fastapi import FastAPI
from . import models
from .database import engine
from .routes import users, records, summary

# Create DB schemas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Data Processing and Access Control Backend")

app.include_router(users.router)
app.include_router(records.router)
app.include_router(summary.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Finance Dashboard Backend. Check /docs for API documentation."}