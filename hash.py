import hashlib
import json

# Function to hash text with a salt
def hash256(text, salt):
    text = text.encode()
    salt = salt.encode()
    return hashlib.sha256(text + salt).hexdigest()

# Secret key used for generating additional salt
SECRET_KEY = "s3cr3t"

# Function to generate a password hash with a salt
def password(plaintext, salt):
    salt1 = hash256(SECRET_KEY, salt)
    hsh = hash256(plaintext, salt1)
    return "".join((salt1, hsh))

# Function to generate a user-friendly password
def generate_password(plaintext, salt, include_special_chars, length=10):
    alphabet = (
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '0123456789'
    )
    if include_special_chars:
        alphabet += '!@#$%^&*()-_'

    hexdig = password(plaintext, salt)
    num = int(hexdig, 16)

    num_chars = len(alphabet)
    chars = []

    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(alphabet[idx])

    return ''.join(chars)

# Function to write data to a JSON file
def write_to_json_file(file_name, data):
    with open(file_name, 'w') as fp:
        json.dump(data, fp, indent=4)

# Main execution block
if __name__ == "__main__":
    # Get user inputs
    username = input("Enter username: ")
    website = input("Enter website name: ")
    include_special_chars = int(input("Enter 1 if you want special characters, or 0 otherwise: "))

    # Generate the password
    generated_password = generate_password(username, website, include_special_chars)

    # Print the generated password
    print(f"Generated Password: {generated_password}")

    # Prepare data to save
    data = {
        "username": username,
        "website": website,
        "password": generated_password
    }

    # Save the data to a JSON file
    output_file = 'data.json'
    write_to_json_file(output_file, data)
    print(f"Password saved to {output_file}")
