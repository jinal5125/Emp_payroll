import json

def load_employees():
    try:
        with open("employees.json","r") as f:
            return json.load(f)
    except:
        return []

def save_employees(data):
    with open("employees.json","w") as f:
        json.dump(data,f,indent=4)

def load_attendance():
    try:
        with open("attendance.json","r") as f:
            return json.load(f)
    except:
        return []

def save_attendance(data):
    with open("attendance.json","w") as f:
        json.dump(data,f,indent=4)


def admin_panel():
    while True:
        print("\n========== ADMIN PANEL ==========")
        print("1. Register Employee")
        print("2. Mark Attendance")
        print("3. View Employee")
        print("4. View Attendance")
        print("5. Generate Payroll")   
        print("6. View Report")
        print("7. Back to Main")


        choice = input("Enter choice: ")

        if choice == "1":
            register_employee()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            view_employees()
        elif choice == "4":
            view_attendance()
        elif choice == "5":
            generate_payroll()
        elif choice == "6":
            view_report()
        elif choice == "7":
            break


# 1.--------------admin registration---------------------
def register_employee():
    print("\n--- REGISTER EMPLOYEE ---")
    employees = load_employees()

    emp_id = int(input("Enter Employee ID: "))
    name = input("Enter Employee Name: ")
    salary = int(input("Enter Monthly Salary: "))
    joining_date = input("Enter Joining Date (DD-MM-YYYY): ")

    employees.append({
        "id": emp_id,
        "name": name,
        "salary": salary,
        "password": None,
        "joining_date": joining_date
    })

    save_employees(employees)
    print("Employee Registered Successfully!")

# 2.------------------mark attendance-----------------------
def mark_attendance():
    print("\n--- MARK ATTENDANCE ---")

    employees = load_employees()
    if not employees:
        print("No employees found! Register employees first.")
        return

    emp_id = int(input("Enter Employee ID: "))

    # validate employee
    found = False
    for emp in employees:
        if emp["id"] == emp_id:
            found = True
            break

    if not found:
        print("Invalid Employee ID!")
        return

    date = input("Enter Date (DD-MM-YYYY): ")
    status = input("Enter Status (P/A/L): ").upper()

    if status not in ["P", "A", "L"]:
        print("Invalid Status! Use P (Present), A (Absent) or L (Leave)")
        return

    attendance = load_attendance()
    attendance.append({
        "id": emp_id,
        "date": date,
        "status": status
    })

    save_attendance(attendance)
    print("Attendance Marked Successfully!")

    
# 3.-------------------view employee----------------------------

def view_employees():
    print("\n--- EMPLOYEE LIST ---")

    employees = load_employees()
    if not employees:
        print("No employees found!")
        return

    for emp in employees:
        print(f"ID: {emp['id']} | Name: {emp['name']} | Salary: {emp['salary']}")


# 4.--------------------View attendance-------------------------------

def view_attendance():
    print("\n--- ATTENDANCE RECORD ---")

    attendance = load_attendance()
    if not attendance:
        print("No attendance records found!")
        return

    for att in attendance:
        print(f"ID: {att['id']} | Date: {att['date']} | Status: {att['status']}")


# 5.--------------------Genrate payroll-----------------------

def generate_payroll():
    print("\n--- GENERATE PAYROLL ---")

    employees = load_employees()
    attendance = load_attendance()

    if not employees:
        print("No employees found!")
        return

    emp_id = int(input("Enter Employee ID: "))

    # find employee data
    emp = None
    for e in employees:
        if e["id"] == emp_id:
            emp = e
            break

    if emp is None:
        print("Invalid Employee ID!")
        return

    # count attendance
    present = 0
    absent = 0
    leave = 0

    for att in attendance:
        if att["id"] == emp_id:
            if att["status"] == "P":
                present += 1
            elif att["status"] == "A":
                absent += 1
            elif att["status"] == "L":
                leave += 1

    # salary calculation
    per_day = emp["salary"] / 30
    net_salary = (present + leave) * per_day

    print("\n--- PAYROLL RESULT ---")
    print(f"Employee Name: {emp['name']}")
    print(f"Monthly Salary: {emp['salary']}")
    print(f"Present Days: {present}")
    print(f"Absent Days: {absent}")
    print(f"Leave Days: {leave}")
    print(f"Net Salary: {net_salary}")



# 6.---------------------View report----------------------------

def view_report():
    print("\n--- VIEW PAYROLL REPORT ---")

    employees = load_employees()
    attendance = load_attendance()

    if not employees:
        print("No employees found!")
        return

    emp_id = int(input("Enter Employee ID: "))

    # Employee find
    emp = None
    for e in employees:
        if e["id"] == emp_id:
            emp = e
            break

    if emp is None:
        print("Invalid Employee ID!")
        return

    present = 0
    absent = 0
    leave = 0

    for att in attendance:
        if att["id"] == emp_id:
            if att["status"] == "P":
                present += 1
            elif att["status"] == "A":
                absent += 1
            elif att["status"] == "L":
                leave += 1

    per_day = emp["salary"] / 30
    net_salary = (present + leave) * per_day

    print("\n===== SALARY REPORT =====")
    print(f"Employee ID   : {emp['id']}")
    print(f"Employee Name : {emp['name']}")
    print(f"Monthly Salary: {emp['salary']}")
    print(f"Present Days  : {present}")
    print(f"Leave Days    : {leave}")
    print(f"Absent Days   : {absent}")
    print(f"Net Salary    : {round(net_salary,2)}")
    print("==========================")


#--------------------------7.manage leave request--------------------------------


