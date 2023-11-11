import requests

class LicenseManager:
    def __init__(self, server_url):
        self.server_url = server_url

    def _make_request(self, key):
        if not isinstance(key, str) or not key:
            raise ValueError("The input parameters were incorrect.")
        try:
            response = requests.get(f"{self.server_url}/api/keys/{key}")
            
            if response.status_code == 200:
                return response.json(), None
            elif response.status_code == 404:
                return None, "Could not find the key."
            elif response.status_code == 400:
                return None, "The input parameters were incorrect."
            else:
                return None, f"Server responded with: {response.status_code}"
     
        except requests.exceptions.RequestException as e:
            return None, str(e)


    def is_expired(self, key):
        data, error = self._make_request(key)
        if error:
            return True, error
        if 'isExpired' not in data:
            return True, "'isExpired' not found in response data"
        
        if data['isExpired']:
            return True, "The key is expired"
        
        return False, "The key is not expired"


    def get_key_info(self, key):
        data, error = self._make_request(key)
        if error:
            return None, error
        return data, "Success"
