import json
from license_package import LicenseManager

license_manager = LicenseManager("http://localhost:5000")

# Getting Key Info
key_info, error = license_manager.get_key_info("CDFC-E5B0-1A5B-9F94")
if key_info is not None:
    formatted_key_info = json.dumps(key_info, indent=4)
    print(f"Key Info: {formatted_key_info}")
else:
    print(f"Error: {error}")
