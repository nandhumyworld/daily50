# Program 1: Check if a number is even or odd and also check a list of numbers

# Single number check
num = int(input("Enter a number to check if it's even or odd: "))
if num % 2 == 0:
    print(f"{num} is Even.")
else:
    print(f"{num} is Odd.")

# Check a list of numbers
number_list = [3, 12, 7, 20, 9]
print("\nChecking list of numbers:")
for n in number_list:
    result = "Even" if n % 2 == 0 else "Odd"
    print(f"{n} is {result}")
