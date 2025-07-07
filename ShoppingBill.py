# Program 3: Calculate total cost of 3 items including tax

# Input prices for 3 items
item1 = float(input("Enter price of item 1: ₹"))
item2 = float(input("Enter price of item 2: ₹"))
item3 = float(input("Enter price of item 3: ₹"))

# Input tax percentage
tax_percent = float(input("Enter tax percentage: "))

# Total without tax
subtotal = item1 + item2 + item3

# Calculate tax
tax = (tax_percent / 100) * subtotal

# Final total
total = subtotal + tax

print(f"\nSubtotal: ₹{subtotal:.2f}")
print(f"Tax (@{tax_percent}%): ₹{tax:.2f}")
print(f"Total amount to pay: ₹{total:.2f}")
