from faker import Faker
import pandas as pd
import csv

fake = Faker()

num_employees = 5000
employees = []

for i in range(1, num_employees + 1):
    employee = {
        "employee_id": i,
        "name": fake.name()
    }
    employees.append(employee)

employee_df = pd.DataFrame(employees)

employee_df.to_csv('employees.csv', index=False)

print(f"Generated {num_employees} employees")
print("Sample data:")
print(employee_df.head(10))
print(f"\nData saved to employees.csv")