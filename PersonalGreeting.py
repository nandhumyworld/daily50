# Ask user for inputs
name = input("What is your name? ")
age = input("How old are you? ")
favorite_color = input("What is your favorite color? ")

# Create a personalized message
message = f"Hello {name}! You're {age} years old and love the color {favorite_color}. That's awesome!"

# Print the message
print("\n" + message)


name = "Nandhu"
print(f"Hello {name}")     # f-string

#print(r"C:\Users\Nandhu")   # raw string

print(b"hello")             # bytes

print(u"hello")             # unicode (Python 2/3)
