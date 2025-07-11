import matplotlib.pyplot as plt

# Day 9/50 - AI Python Challenge
# Sum Calculator : Find sum of all numbers from 1 to n using a loop.
# Use filename as SumCalculator.py
# Our Goal : Use any AI tool to generate the script and execute the script without issue

def sum_using_loop(n):
    """Calculate sum of numbers from 1 to n using a loop"""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def main():
    # Get input from user
    try:
        n = int(input("Enter a positive integer n: "))
        if n <= 0:
            print("Please enter a positive integer.")
            return
    except ValueError:
        print("Please enter a valid integer.")
        return
    
    # Calculate sum using loop
    result = sum_using_loop(n)
    print(f"Sum of numbers from 1 to {n} = {result}")
    
    # Generate data for plotting
    x_values = []
    y_values = []
    
    # Calculate sums for values from 1 to n
    for i in range(1, n + 1):
        x_values.append(i)
        y_values.append(sum_using_loop(i))
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, 'b-', linewidth=2, marker='o', markersize=4)
    plt.title(f'Sum of Numbers from 1 to i (where i goes from 1 to {n})')
    plt.xlabel('n')
    plt.ylabel('Sum (1 + 2 + ... + n)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Add annotation for the final result
    plt.annotate(f'Sum(1 to {n}) = {result}', 
                xy=(n, result), 
                xytext=(n*0.7, result*0.8),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    plt.show()
    
    # Also show the mathematical formula verification
    formula_result = n * (n + 1) // 2
    print(f"Verification using formula n(n+1)/2 = {formula_result}")
    print(f"Results match: {result == formula_result}")

if __name__ == "__main__":
    main()