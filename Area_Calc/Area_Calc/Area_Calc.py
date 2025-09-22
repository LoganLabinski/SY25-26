def flag():
    for i in range(3):
        print("******==========")
    for i in range(3):
        print("================")


print("hello")
name = input("Enter your name: ")
print("Hello " + name)
age= int(input("Enter your age: "))
if age >= 18:
    print("You are eligible to vote")
    flag()
else:
    print("You are not eligible to vote")