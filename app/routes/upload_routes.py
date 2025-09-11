# app/routes/upload_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, status
import csv
import io
from datetime import datetime
from typing import List, Tuple, Any
import asyncpg

router = APIRouter()

async def _read_csv_text(upload_file: UploadFile) -> str:
    """
    Read upload file into text. Using .read() is fine for CSVs of typical sizes.
    If you expect extremely large files (many 100s of MB), you can implement
    chunked streaming parsing — but COPY requires building batches anyway.
    """
    raw = await upload_file.read()
    # handle BOM if present
    return raw.decode("utf-8-sig")


async def _copy_in_batches(
    pool: asyncpg.pool.Pool,
    table: str,
    columns: List[str],
    records_iter,
    batch_size: int = 10000,
) -> int:
    """
    records_iter -> an iterator of tuples (in the same order as `columns`)
    Use pool.acquire() to get connection and call copy_records_to_table in batches.
    """
    inserted = 0
    async with pool.acquire() as conn:
        batch = []
        for rec in records_iter:
            batch.append(rec)
            if len(batch) >= batch_size:
                await conn.copy_records_to_table(table, records=batch, columns=columns)
                inserted += len(batch)
                batch.clear()
        if batch:
            await conn.copy_records_to_table(table, records=batch, columns=columns)
            inserted += len(batch)
    return inserted


@router.post("/upload/employees", status_code=status.HTTP_201_CREATED)
async def upload_employees(request: Request, file: UploadFile = File(...)):
    """
    Expects CSV with headers: id,name,department,current_shift
    id may be omitted if you want DB to generate PK (remove id column from columns below).
    """
    text = await _read_csv_text(file)
    sio = io.StringIO(text)
    reader = csv.DictReader(sio)
    required = ["id", "name", "department", "current_shift"]
    if not set(required).issubset(reader.fieldnames or []):
        raise HTTPException(status_code=400, detail=f"CSV headers must include: {required}")

    # build iterator of tuples with proper types
    def gen():
        for row in reader:
            # convert empty strings to None
            _id = int(row["id"]) if row.get("id") not in (None, "", "NULL") else None
            name = row["name"] or None
            dept = row.get("department") or None
            shift = row.get("current_shift") or None
            yield (_id, name, dept, shift)

    pool = request.app.state.pg_pool
    # table name must match your model __tablename__
    inserted = await _copy_in_batches(pool, "employees", ["id", "name", "department", "current_shift"], gen())
    return {"inserted": inserted}


@router.post("/upload/shifts", status_code=status.HTTP_201_CREATED)
async def upload_shifts(request: Request, file: UploadFile = File(...)):
    """
    Expects CSV headers: employee_id,week,shift_type
    """
    text = await _read_csv_text(file)
    sio = io.StringIO(text)
    reader = csv.DictReader(sio)
    required = ["employee_id", "week", "shift_type"]
    if not set(required).issubset(reader.fieldnames or []):
        raise HTTPException(status_code=400, detail=f"CSV headers must include: {required}")

    def gen():
        for row in reader:
            yield (int(row["employee_id"]), int(row["week"]), row["shift_type"])

    pool = request.app.state.pg_pool
    inserted = await _copy_in_batches(pool, "shifts", ["employee_id", "week", "shift_type"], gen())
    return {"inserted": inserted}


@router.post("/upload/attendance", status_code=status.HTTP_201_CREATED)
async def upload_attendance(request: Request, file: UploadFile = File(...)):
    """
    Expects CSV headers: employee_id,login_time,logout_time
    login_time / logout_time should be ISO format: YYYY-MM-DDTHH:MM:SS (timezone optional)
    """
    text = await _read_csv_text(file)
    sio = io.StringIO(text)
    reader = csv.DictReader(sio)
    required = ["employee_id", "login_time", "logout_time"]
    if not set(required).issubset(reader.fieldnames or []):
        raise HTTPException(status_code=400, detail=f"CSV headers must include: {required}")

    def parse_iso(dt_str: str):
        if not dt_str or dt_str.strip() == "":
            return None
        try:
            # Python 3.11+ supports fromisoformat with more cases;
            # this will handle common ISO formats without timezone or with +HH:MM
            # If you need more robust parsing, consider dateutil.parser.parse
            return datetime.fromisoformat(dt_str)
        except Exception:
            # try fallback for space-separated format
            try:
                return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            except Exception:
                raise HTTPException(status_code=400, detail=f"Invalid datetime format: {dt_str}")

    def gen():
        for row in reader:
            emp_id = int(row["employee_id"])
            login = parse_iso(row["login_time"])
            logout = parse_iso(row["logout_time"]) if row.get("logout_time") else None
            yield (emp_id, login, logout)

    pool = request.app.state.pg_pool
    inserted = await _copy_in_batches(pool, "attendance", ["employee_id", "login_time", "logout_time"], gen())
    return {"inserted": inserted}
