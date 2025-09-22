# This program calculates the area and perimeter of a rectangle
# and draws a simple text-based rectangle.
# It contains a few bugs that need to be fixed.

def calculate_rectangle_properties(length, width):
    """
    Calculates the area and perimeter of a rectangle.
    """
    # Bug 1:     area = length * width
    area = length * width
    perimeter = 2 * (length + width) 
    return area, perimeter

def draw_rectangle(length, width):
    """
    Draws a simple ASCII rectangle of a given length and width.
    """
    if length <= 0 or width <= 0:
        return "Length and width must be positive numbers."

    rectangle_art = ""
    # Top border
    rectangle_art += "*" * width + "\n" 

    # Bug 2: The loop for the middle rows is incorrect.
    for i in range(length - 2):
        rectangle_art += "*" * width + "\n"

    # Bottom border
    rectangle_art += "*" * width + "\n"

    return rectangle_art

def main():
    while True:
        try:
            user_length = int(input("Enter the length of the rectangle: "))
            user_width = int(input("Enter the width of the rectangle: "))
            break
        except ValueError:
            print("Invalid input. Please enter numbers.")

    area, perimeter = calculate_rectangle_properties(user_length, user_width)
    rectangle_art = draw_rectangle(user_length, user_width)

    # Bug 3: 
    print(f"The area of the rectangle is: {area}")
    print(f"The perimeter of the rectangle is: {perimeter}")

    print("\nYour rectangle:")
    print(rectangle_art)

main()


