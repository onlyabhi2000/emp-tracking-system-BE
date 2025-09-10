from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import engine, Base
app = FastAPI()

@app.get("/")
def root_check():
    return {"message" :"Working fine....."}


from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.shift import Shift

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Employee Attendance Tracker is running "}