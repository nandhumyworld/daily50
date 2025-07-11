def check_password_length(password, min_length=8):
    """
    Check if a password meets the minimum length requirement.
    
    Args:
        password (str): The password to check
        min_length (int): Minimum required length (default: 8)
    
    Returns:
        bool: True if password meets minimum length, False otherwise
    """
    return len(password) >= min_length

def validate_password_with_feedback(password, min_length=8):
    """
    Check password length and provide feedback message.
    
    Args:
        password (str): The password to check
        min_length (int): Minimum required length (default: 8)
    
    Returns:
        tuple: (is_valid, feedback_message)
    """
    if len(password) >= min_length:
        return True, f"Password is valid! Length: {len(password)} characters"
    else:
        return False, f"Password too short! Current: {len(password)}, Required: {min_length}"

# Example usage
if __name__ == "__main__":
    # Test passwords
    test_passwords = [
        "123",
        "password",
        "mySecurePass123",
        "short",
        "ThisIsALongPassword123!"
    ]
    
    print("Password Length Validation Results:")
    print("-" * 40)
    
    for pwd in test_passwords:
        is_valid, message = validate_password_with_feedback(pwd)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status}: '{pwd}' - {message}")
    
    print("\n" + "=" * 40)
    
    # Interactive password checker
    while True:
        user_password = input("\nEnter a password to check (or 'quit' to exit): ")
        if user_password.lower() == 'quit':
            break
        
        is_valid, message = validate_password_with_feedback(user_password)
        print(f"Result: {message}")
        
        if is_valid:
            print("🎉 Password meets length requirements!")
        else:
            print("❌ Password needs to be longer.")