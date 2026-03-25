while True:
    print("What do you want to do?")  
    print("1. Add an expense")  
    print("2. View expenses")
    print("3. Erase an expense")
    print("4. View total of all expenses")  
    print("5. Search expenses") 
    print("6. Exit")  
    choice = input("Enter 1, 2, 3, 4, 5, or 6: ")  

    if choice == "1":  
     # Ask the user for expense details  
        date = input("Enter date (YYYY-MM-DD): ")  
        amount = input("Enter amount: ")  
        category = input("Enter category: ")  
        location = input("Enter expense location: ")  
  
# Format the data as a single line, separated by commas  
        line = f"{date},{amount},{category},{location}\n"  
  
# Append the expense to the file  
        with open("expenses.txt", "a") as file:  
            file.write(line)  
  
        print("Expense added!")  
 
    elif choice == "2":  
        with open("expenses.txt", "r") as file:  
            for line in file:  
                print(line.strip())  

        pass
    elif choice == "3":  
        # Read expenses from file  
        with open("expenses.txt", "r") as file:  
            expenses = file.readlines()  
  
# Show all expenses with a number  
        print("Your current expenses:")  
        for idx, expense in enumerate(expenses):  
            print(f"{idx + 1}: {expense.strip()}")  
  
# Ask which number to erase  
        try:  
            to_erase = int(input("Enter the number of the expense to erase: ")) - 1  
            if 0 <= to_erase <= len(expenses):  
                expenses.pop(to_erase)  
                print("Expense erased.")  
            else:  
                print("Invalid number.")  
        except ValueError:  
            print("Please enter a valid number.")  
  
# Write back the updated list  
        with open("expenses.txt", "w") as file:  
            file.writelines(expenses)  
        pass

    elif choice == "4":
        total = 0.0  
        with open("expenses.txt", "r") as file:  
            for line in file:  
                parts = line.strip().split(",")  
                if len(parts) >= 2:  
                    try:  
                        amount = float(parts[1])  
                        total += amount  
                    except ValueError:  
                        pass  # skip lines with invalid numbers  
  
        print(f"Total expenses: ${total:.2f}")  
    elif choice == "5":    
        keyword = input("Enter a keyword to search for: ")  
        with open("expenses.txt", "r") as file:  
            found = False  
            for line in file:  
                if keyword.lower() in line.lower():  
                    print(line.strip())  
                    found = True  
            if not found:  
                print("No expenses found matching that keyword.")
    elif choice == "6":  
        print("Goodbye!")  
        break  
    else:  
        print("Invalid choice")  
        pass
