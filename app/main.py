from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncpg

from app.core.db import engine, Base, DATABASE_URL
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.shift import Shift
from app.routes.upload_routes import router as upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    pg_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

    # Create asyncpg pool for fast CSV inserts
    app.state.pg_pool = await asyncpg.create_pool(pg_url, min_size=2, max_size=10)

    try:
        yield
    finally:
        await app.state.pg_pool.close()
        await engine.dispose()


# Init FastAPI app with lifespan
app = FastAPI(lifespan=lifespan, title="Employee Attendance Tracker")

# Include CSV upload routes
app.include_router(upload_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Employee Attendance Tracker is running"}
