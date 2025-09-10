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

df = pd.read_csv('D:\Emp_track_system\data_generation\employees.csv')[['employee_id', 'name']]
data = list(df.itertuples(index=False, name=None))

execute_values(cur, "INSERT INTO employees (employee_id, name) VALUES %s", data)

conn.commit()
cur.close()
conn.close()