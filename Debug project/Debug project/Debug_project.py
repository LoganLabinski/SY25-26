# This is a simple program to calculate a user's age category based on their input.
# It contains a few bugs that need to be fixed.

# Function to determine the age category
def get_age_category(age):
  # Bug 1: Incorrect comparison operator.
  # The program should check if age is a valid number.
  if age > 0:
    print("Please enter a valid age as a number.")
    return None

  # Bug 2: Incorrect logic in if-elif-else statements.
  # The conditions are overlapping and will cause issues.
  if age < 18 and age > 0:
    return "Child"
  elif age >= 18 and age < 65:
    return "Adult"
  elif age >= 65:
    return "Senior"
  elif age < 0:
    return "Invalid age" # This line may not be reachable

# Main part of the program
def main():
  # Bug 3: Incorrect variable assignment and type conversion.
  # The user input needs to be correctly converted to a number.
  user_age = int(input("Please enter your age: "))

  category = get_age_category(user_age)

  # Bug 4: Incorrect f-string usage.
  # The program should correctly format the output string.
  if category:
    print(f"You are a {category}.")

# Call the main function to run the program
main()

