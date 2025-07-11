
def compare_numbers(num1, num2):
    """
    Compare two numbers and return the comparison result
    
    Args:
        num1: First number
        num2: Second number
    
    Returns:
        str: Comparison result
    """
    if num1 > num2:
        return f"{num1} is greater than {num2}"
    elif num1 < num2:
        return f"{num1} is less than {num2}"
    else:
        return f"{num1} is equal to {num2}"

def get_number_input(prompt):
    """
    Get a valid number input from user
    
    Args:
        prompt: Input prompt message
    
    Returns:
        float: Valid number
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# Main program
if __name__ == "__main__":
    print("Number Comparison Program")
    print("-" * 25)
    
    # Get input from user
    first_number = get_number_input("Enter the first number: ")
    second_number = get_number_input("Enter the second number: ")
    
    # Compare and display result
    result = compare_numbers(first_number, second_number)
    print(f"\nResult: {result}")
    
    # Additional comparison details
    print("\nDetailed comparison:")
    if first_number > second_number:
        difference = first_number - second_number
        print(f"• {first_number} is larger by {difference}")
    elif first_number < second_number:
        difference = second_number - first_number
        print(f"• {second_number} is larger by {difference}")
    else:
        print("• Both numbers are identical")