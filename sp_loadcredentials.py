import json

# Global variable to store credentials
superpumped_credentials = None

def superpumped_load_credentials():
    global superpumped_credentials
    try:
        with open('credentials.json', 'r') as f:
            superpumped_credentials = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            "credentials.json not found. Please copy credentials.json.example "
            "to credentials.json and fill in your credentials."
        )
    return superpumped_credentials

# Load credentials when module is imported
superpumped_load_credentials()