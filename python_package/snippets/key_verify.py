from license_package import LicenseManager

license_manager = LicenseManager("http://127.0.0.1:5000")

# Verifying a Key
is_expired, error = license_manager.is_expired("CDFC-E5B0-1A5B-9F94")
if not is_expired:
    print(f"The key is valid")
else:
    print(f"Error: {error}")