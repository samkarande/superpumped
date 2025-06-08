from skyflow.service_account import generate_bearer_token
from skyflow.vault import Client, Configuration, InsertOptions
from skyflow.errors import SkyflowError
import json

def insert_passenger_record(record, credentials_path, vault_id, vault_url):
    try:
        # Generate Bearer token from credentials file
        bearer_token, _ = generate_bearer_token(credentials_path)

        # Configure Skyflow Vault client
        config = Configuration(vault_id, vault_url, lambda: bearer_token)
        client = Client(config)
        option = InsertOptions(True)
        # Prepare the insert payload
        data = {
            "records": [
                {
                    "table": "passenger",
                    "fields": record
                }
            ]
        }

        # Insert the record into the ride table
        response = client.insert(data, options=option)

        # Return the insert response
        return response

    except SkyflowError as e:
        print(f"Skyflow Error: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

def main():
    try:
        # Configuration
        credentials_path = "bearer-token-cred.json"  # Path to your Skyflow credentials file
        vault_id = "o0ec618918544fea843e5975bd516e8d"
        vault_url = "https://ebfc9bee4242.vault.skyflowapis.com"

        # Example record to insert (matches the schema from the cURL)
        record = {
            "passengerid": 1010,
            "fname": "Soo-jin",
            "lname": "Park",
            "state" : "CA",
            "country": "US",
            "phone": "+14088294532",
            "email": "park@gmail.com",
            "address": "29 oark st, san hose, CA 94010"
        }

        # Insert the record
        result = insert_passenger_record(record, credentials_path, vault_id, vault_url)

        # Print the insert response
        print("Insert Response:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()