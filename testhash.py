import bcrypt

# Example password to hash
password = "mysecretpassword"

# Generate a salt and hash the password
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode(), salt)

print(f"Salt and hashed password: {hashed_password.decode()}")

# To verify
is_correct = bcrypt.checkpw(password.encode(), hashed_password)
print(f"Password is correct: {is_correct}")
