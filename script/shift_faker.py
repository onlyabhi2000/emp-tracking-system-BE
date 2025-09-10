from faker import Faker
import pandas as pd
import csv

fake = Faker()

num_employees = 5000
num_weeks = 4
shift_types = ['morning', 'evening', 'night']
shifts = []

for week in range(1, num_weeks + 1):
    for employee_id in range(1, num_employees + 1):
        shift = {
            "shift_id": len(shifts) + 1,
            "employee_id": employee_id,
            "shift_type": fake.random_element(elements=shift_types),
            "week_number": week
        }
        shifts.append(shift)

shift_df = pd.DataFrame(shifts)

shift_df.to_csv('employee_shifts.csv', index=False)

print(f"Generated {len(shifts)} shift records")
print("Sample data:")
print(shift_df.head(10))
print(f"\nData saved to employee_shifts.csv")