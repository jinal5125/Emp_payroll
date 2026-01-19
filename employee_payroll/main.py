from admin_panel import admin_panel
from user_panel import user_panel

def main():
    while True:
        print("============== PAYROLL SYSTEM ==============")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_panel()
        elif choice == "2":
            user_panel()
        elif choice == "3":
            print("Exiting System...")
            break
        else:
            print("Invalid choice!")

main()


