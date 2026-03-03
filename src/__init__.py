from fastapi import FastAPI
from .expense.routes import expense_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()

    yield
    print("Shutting down...")


version = "0.1.0"
app = FastAPI(
    title="FinFlow API",
    description="An API for managing expenses",
    version=version,
    lifespan=lifespan,
)

app.include_router(expense_router, prefix="/expenses", tags=["expenses"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn src.__init__:app --reload --port 8000
