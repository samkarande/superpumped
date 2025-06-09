from skyflow.service_account import generate_bearer_token
from skyflow.vault import Client, Configuration, InsertOptions
from skyflow.errors import SkyflowError
import json
from datetime import datetime, timedelta
import random

def create_new_ride_records(count):
    rideid_start = 10000+ datetime.now().microsecond
    #str(datetime.now()+ timedelta(minutes=10))
    current_time = datetime.now()
    ridestarttime = current_time.strftime("%Y-%m-%dT%H:%M:%S")
    current_time += timedelta(minutes=10)
    rideendtime = current_time.strftime("%Y-%m-%dT%H:%M:%S")



    #rides = []
    #for i in range(count):
    ride = {
        "rideid": rideid_start,
        "driverid": random.randint(200, 210),
        "passengerid": random.randint(2000, 2010),
        "ridestarttime": ridestarttime,
        "rideendtime": rideendtime,
        "active": random.choice([True, False]),
        "flagged": random.choice([True, False]),
        "state": random.choice(["KA", "MH", "KA", "MH"]),
        "startaddress": "123 summer St",
        "endaddress": "456 Oak Ave",
        "zipcode": random.choice(["400001", "400002", "560100", "560050"]),
        "country": "IN",
        "drivephone": str(random.randint(3000000000, 9000000000)),
        "passengerphone": str(random.randint(3000000000, 9000000000))
    }
    #    rides.append(ride)
    return ride

def insert_ride_record(record, credentials_path, vault_id, vault_url):
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
                    "table": "ride",
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
        ## Superpumped US vault
        #credentials_path = "bearer-token-cred.json"  # Path to your Skyflow credentials file
        #vault_id = "o0ec618918544fea843e5975bd516e8d"
        #vault_url = "https://ebfc9bee4242.vault.skyflowapis.com"

        ## Superpumped IN vault
        credentials_path = "in-bearer-token-cred.json"  # Path to your Skyflow credentials file
        vault_id = "c323aef5487c4e5ca482e865a430d2e3"
        vault_url = "https://ebfc9bee4242.vault.skyflowapis.com"

        # Example record to insert (matches the schema from the cURL)
        #record = {
        #    "rideid": 10003,
        #    "driverid": 103,
        #    "passengerid": 1003,
        #    "ridestarttime": "2025-06-07T13:40:00",
        #    "rideendtime": "2025-06-07T15:40:00",
        #    "active": True,
        #    "flagged": True,
        #    "state": "CA",
        #    "startaddress": "123 summer St",
        #    "endaddress": "456 Oak Ave",
        #    "zipcode": "90210",
        #    "country": "US",
        #    "drivephone": "+1-630-321-0202",
        #    "passengerphone": "+1-555-987-0101"
        #}

        # Insert the record
        for i in range(20):

            record = create_new_ride_records(1)
            #print(json.dumps(record, indent=2))

            result = insert_ride_record(record, credentials_path, vault_id, vault_url)
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()