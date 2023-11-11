import json
from license_package import LicenseManager

license_manager = LicenseManager("http://localhost:5000")

print("Authentificate to continue")
key = str(input("Enter your key: "))

# Verifying a Key
is_expired, error = license_manager.is_expired(key)
if is_expired:
    print(f"Error: {error}")
    exit()

print("The key is valid")

# Getting Key Info
key_info, response = license_manager.get_key_info(key)
if key_info is not None:
    formatted_key_info = json.dumps(key_info, indent=4)
    print(f"Key Info:\n{formatted_key_info}")
