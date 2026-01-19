from admin_panel import load_employees, save_employees , load_attendance
from datetime import datetime

def user_panel():
    while True:
        print("\n========== USER PANEL ==========")
        print("1. Login")
        print("2. Back to Main")

        choice = input("Enter choice: ")

        if choice == "1":
            user_login()
        elif choice == "2":
            break
        else:
            print("Invalid choice!")


#--------------------------User login--------------------------------


def user_login():
    print("\n--- USER LOGIN ---")
    employees = load_employees()

    # employees.json empty check
    if not employees:
        print("No employees found! Contact admin.")
        return

    emp_id_input = input("Enter Employee ID: ")

    # numeric check
    if not emp_id_input.isdigit():
        print("ID must be a number!")
        return

    emp_id = int(emp_id_input)

    # find employee
    emp = None
    for e in employees:
        if e["id"] == emp_id:
            emp = e
            break

    if emp is None:
        print("Invalid Employee ID!")
        return

    # first time login
    if emp["password"] is None:
        print("First time login! Please set your password.")
        set_new_password(emp, employees)
        print("Password set successfully!\n")
        user_login()
        return

    # normal login
    password = input("Enter Password: ")

    if password == emp["password"]:
        print("Login Successful!")
        user_dashboard(emp)
    else:
        print("Invalid Password!")


#-------------------set password for employee----------------------


def set_new_password(emp, employees):
    print("\n--- SET NEW PASSWORD ---")

    new_pass = input("Enter New Password: ")
    confirm = input("Confirm Password: ")

    if new_pass != confirm:
        print("Passwords do not match!")
        return   
    emp["password"] = new_pass
    save_employees(employees)
    #print("Password Set Successfully!")


#-------------------------Dashbord-------------------------

def user_dashboard(emp):
    while True:
        print("\n========== USER DASHBOARD ==========")
        print("1. View Attendance")
        print("2. View Salary Report")
        print("3. View Profile")
        print("4. Change Password")
        print("5. Experiance")
        print("6. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            user_view_attendance(emp)
        elif choice == "2":
            user_view_salary(emp)
        elif choice == "3":
            user_view_profile(emp)
        elif choice == "4":
            user_change_password(emp)
        elif choice == "5":
            y, m, d = calculate_experience(emp["joining_date"])
            print(f"Experience   : {y} Years {m} Months {d} Days")
        elif choice == "6":
            pass
        elif choice == "7":
            pass
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

#----------------------1.view attendance----------------------------

from admin_panel import load_attendance

def user_view_attendance(emp):
    print("\n--- YOUR ATTENDANCE ---")
    
    attendance = load_attendance()

    if not attendance:
        print("No attendance records found!")
        return

    records = [a for a in attendance if a["id"] == emp["id"]]

    if not records:
        print("No attendance found for your account!")
        return

    for r in records:
        print(f"Date: {r['date']} | Status: {r['status']}")


#---------------------------- 2.View salary report---------------------------------

def user_view_salary(emp):
    print("\n--- SALARY REPORT ---")

    salary = emp["salary"]
    attendance = load_attendance()

    if not attendance:
        print("No attendance available!")
        return

    # Filter specific employee attendance
    records = [a for a in attendance if a["id"] == emp["id"]]

    if not records:
        print("No attendance found for your account!")
        return

    # Count statuses
    present = sum(1 for r in records if r["status"] == "P")
    absent  = sum(1 for r in records if r["status"] == "A")
    leave   = sum(1 for r in records if r["status"] == "L")

    # Salary calculations
    total_days = present + absent + leave
    per_day = salary / 30
    net_salary = present * per_day   # only paid for present

    # Display report
    print(f"\nMonthly Salary   : {salary}")
    print(f"Per Day Salary   : {per_day:.2f}")
    print(f"Present Days     : {present}")
    print(f"Absent Days      : {absent}")
    print(f"Leave Days       : {leave}")
    print(f"Total Attendance : {total_days}")
    print(f"Net Salary       : {net_salary:.2f}")

#---------------------3.view profile --------------------------------------

def user_view_profile(emp):
    print("\n--- USER PROFILE ---")
    print(f"Employee ID : {emp['id']}")
    print(f"Name        : {emp['name']}")
    print(f"Salary      : {emp['salary']}")
    print(f"Password    : ******")   
    y, m, d = calculate_experience(emp["joining_date"])
    print(f"Experience   : {y} Years {m} Months {d} Days")



#---------------------4.Change Password-------------------------------------

from admin_panel import save_employees, load_employees

def user_change_password(emp):
    print("\n--- CHANGE PASSWORD ---")

    employees = load_employees()  # load full list

    old = input("Enter Old Password: ")

    if old != emp["password"]:
        print("Incorrect old password!")
        return

    new = input("Enter New Password: ")
    confirm = input("Confirm New Password: ")

    if new != confirm:
        print("Passwords do not match!")
        return

    if new == old:
        print("New password cannot be same as old!")
        return

    # update in main employees list (important part)
    for e in employees:
        if e["id"] == emp["id"]:
            e["password"] = new
            break

    save_employees(employees)
    emp["password"] = new   # update current session (optional)

    print("Password changed successfully! Please login again.\n")

    # logout after password change (company style)
    return "LOGOUT"


# -------------------------Joining date & experiance--------------------------------------

def calculate_experience(join_date_str):
    join_date = datetime.strptime(join_date_str, "%d-%m-%Y")
    today = datetime.today()

    years = today.year - join_date.year
    months = today.month - join_date.month
    days = today.day - join_date.day

    if days < 0:
        months -= 1
        days += 30

    if months < 0:
        years -= 1
        months += 12

    return years, months, days

