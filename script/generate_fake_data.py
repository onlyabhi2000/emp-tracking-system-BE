import csv
import random
import datetime
from faker import Faker

fake = Faker()

N_EMPLOYEES = 5000
N_WEEKS = 4
DAYS_PER_WEEK = 7
SHIFTS = ["morning", "evening", "night"]

# Output files
EMPLOYEE_CSV = "fake_employees.csv"
SHIFT_CSV = "fake_shifts.csv"
ATTENDANCE_CSV = "fake_attendance.csv"


def generate_employees():
    employees = []
    for i in range(1, N_EMPLOYEES + 1):
        employees.append(
            {
                "id": i,
                "name": fake.name(),
                "department": random.choice(["HR", "IT", "Finance", "Sales", "Support"]),
                "current_shift": random.choice(SHIFTS),
            }
        )
    return employees


def generate_shifts(employees):
    shifts = []
    for emp in employees:
        for week in range(1, N_WEEKS + 1):
            shifts.append(
                {
                    "employee_id": emp["id"],
                    "week": week,
                    "shift_type": random.choice(SHIFTS),
                }
            )
    return shifts


def generate_attendance(employees):
    attendances = []
    start_date = datetime.date.today() - datetime.timedelta(weeks=N_WEEKS)

    for emp in employees:
        for week in range(N_WEEKS):
            for day in range(DAYS_PER_WEEK):
                date = start_date + datetime.timedelta(weeks=week, days=day)

                # Random shift login/logout times
                shift = random.choice(SHIFTS)
                if shift == "morning":
                    login = datetime.datetime.combine(date, datetime.time(hour=9, minute=fake.random_int(0, 30)))
                    logout = login + datetime.timedelta(hours=8)
                elif shift == "evening":
                    login = datetime.datetime.combine(date, datetime.time(hour=17, minute=fake.random_int(0, 30)))
                    logout = login + datetime.timedelta(hours=8)
                else:  # night
                    login = datetime.datetime.combine(date, datetime.time(hour=23, minute=fake.random_int(0, 30)))
                    logout = login + datetime.timedelta(hours=8)

                attendances.append(
                    {
                        "employee_id": emp["id"],
                        "login_time": login.isoformat(),
                        "logout_time": logout.isoformat(),
                    }
                )
    return attendances


def write_csv(filename, fieldnames, rows):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    employees = generate_employees()
    shifts = generate_shifts(employees)
    attendance = generate_attendance(employees)

    write_csv(EMPLOYEE_CSV, ["id", "name", "department", "current_shift"], employees)
    write_csv(SHIFT_CSV, ["employee_id", "week", "shift_type"], shifts)
    write_csv(ATTENDANCE_CSV, ["employee_id", "login_time", "logout_time"], attendance)

    print(f"Generated {len(employees)} employees → {EMPLOYEE_CSV}")
    print(f"Generated {len(shifts)} shift records → {SHIFT_CSV}")
    print(f"Generated {len(attendance)} attendance records → {ATTENDANCE_CSV}")
