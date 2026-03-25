# Personal Inventory Manager

inventory = {}

print("-- Personal Inventory Manager --")

while True:
    print("\nOptions: [1] Add [2] Remove [3] List [4] Exit")
    choice = input("Select an option (1-4): ")

    if choice == "1":
        name = input("Enter item name: ").strip().capitalize()
        qty = int(input(f"How many {name}s? "))

        inventory[name] = inventory.get(name, 0) + qty
        print(f"Updated: {name} (Total: {inventory[name]})")

    elif choice == "2":
        name = input("Which item would you like to remove? ").strip().capitalize()

        if name in inventory:
            del inventory[name]
            print(f"Removed {name} from inventory.")
        else:
            print("Item not found in inventory.")

    elif choice == "3":
        print("\n--- Current Inventory ---")
        if inventory:
            for item, qty in inventory.items():
                print(f"- {item}: {qty}")
        else:
            print("Inventory is empty.")

    elif choice == "4":
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid option. Please choose 1-4.")
