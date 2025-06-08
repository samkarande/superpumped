import jwt
import requests
import time
import json

from skyflow.vault import Client, Configuration
from skyflow.errors import SkyflowError

def sp_service_getSignedJWT(credentials_file_path, context=None):
    # Load credentials from the JSON file
    with open(credentials_file_path, 'r') as file:
        creds = json.load(file)

    # Prepare claims for JWT
    claims = {
        "iss": creds["clientID"],
        "key": creds["keyID"],
        "aud": creds["tokenURI"],
        "sub": creds["clientID"],
        "exp": int(time.time()) + 60 * 60  # Token expires in 60 minutes
    }

    # Sign the JWT with the private key
    private_key = creds["privateKey"]
    signed_jwt = jwt.encode(claims, private_key, algorithm="RS256")

    return signed_jwt, creds

def sp_service_getBearerToken(signed_jwt, creds, token=None):
    # Prepare request body for Bearer token
    body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": signed_jwt
    }

    # Make POST request to Skyflow's token endpoint
    token_uri = creds["tokenURI"]
    response = requests.post(token_uri, json=body)

    if response.status_code != 200:
        raise Exception(f"Failed to obtain token: {response.text}")

    # Parse and return the Bearer token
    token_data = response.json()
    return token_data["accessToken"], creds

def run_vault_query(query, bearer_token, vault_url, vault_id):
    # Prepare the query payload
    query_payload = {
        "query": query,
        "vaultID": vault_id
    }

    # Set headers with Bearer token
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    # Make POST request to the Skyflow query endpoint
    query_url = f"{vault_url}/v1/vaults/{vault_id}/query"
    response = requests.post(query_url, json=query_payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Query failed: {response.text}")

    # Return the query results
    return response.json()

def run_vault_query_SDK(query, bearer_token, vault_id, vault_url):
    try:
        # Generate Bearer token from credentials file
        #bearer_token, _ = generate_bearer_token(credentials_path)

        # Configure Skyflow Vault client
        config = Configuration(vault_id, vault_url, lambda: bearer_token)
        client = Client(config)

        querydata = { 
            "query": query
        }
        # Execute the query
        response = client.query(querydata)

        # Return the query results
        return response

    except SkyflowError as e:
        print(f"Skyflow Error: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

def main():
    try:
        # Replace with the path to your credentials.json file
        credentials_path = "superpumped-support-role-credentials.json"
        #credentials_path = "credentials.json"
        # Get the Bearer token
        signed_jwt, creds = getSignedJWT(credentials_path)
        bearer_token, creds = getBearerToken(signed_jwt, creds)

        # Example SQL-like query (modify based on your vault schema)
        query = """
        select * from ride where ride.active = true
        """
        
        # Run the query
        vault_url = creds["vaultURL"]
        vault_id = creds["vaultID"]
        #result = run_vault_query(query, bearer_token, vault_url, vault_id)
        result = run_vault_query_SDK(query, bearer_token, vault_id, vault_url)
        
        # Print the query results
        print("Query Results:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()