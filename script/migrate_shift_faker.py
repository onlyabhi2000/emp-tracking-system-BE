import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

df = pd.read_csv('D:\emp-tracking-system-BE\script\employee_shifts.csv')
data = list(df.itertuples(index=False, name=None))

execute_values(cur, "INSERT INTO shifts (shift_id, employee_id, shift_type, week_number) VALUES %s", data)

conn.commit()
cur.close()
conn.close()