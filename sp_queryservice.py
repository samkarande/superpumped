import jwt
import requests
import time
import json

from skyflow.vault import Client, Configuration, DetokenizeOptions, RedactionType, QueryOptions
from skyflow.errors import SkyflowError
import sp_tokenservice

def sp_getCredentials_path(user):
    credentials_path = ""
    
    if (user == "support"):
        credentials_path = "superpumped-support-role-credentials.json"
    elif (user == "support-context"):
        credentials_path = "superpumped-support-role-credentials-context.json"
    elif (user == "analyst"):
        credentials_path = "superpumped-analyst-cred.json"
    elif( user == "in-support"):
        credentials_path = "Superpumped-IN-Support-cred.json"
    elif (user == "in-analyst"):
        credentials_path = "Superpumped-IN-Analyst-cred.json"
    elif (user == "in-bearer"):
        credentials_path = "in-bearer-token-cred.json"
    else:
        credentials_path = "bearer-token-cred.json"
    
    return credentials_path

def sp_ext_service_get_completed_rides(user, context=None):
    
    credentials_path = sp_getCredentials_path(user)
    
    print("credentials_path: " + credentials_path)

    signed_jwt, creds = sp_tokenservice.sp_service_getSignedJWT(credentials_path, context)
    bearer_token, creds = sp_tokenservice.sp_service_getBearerToken(signed_jwt, creds, context)

    query = """
        select * from ride where ride.active = false
        """
    
    column_redactions = [
        {"column": "drivephone", "redaction": RedactionType.DEFAULT},
        {"column": "passengerphone", "redaction": RedactionType.DEFAULT}
    ]
    
    vault_url = creds["vaultURL"]
    vault_id = creds["vaultID"]
    rides_data = sp_service_query_execute(query, bearer_token, vault_id, vault_url, column_redactions, context)

    #print("rides_data: " + str(rides_data))

    #response = detokenize(rides_data, DetokenizeOptions(continueOnError=True))
    #print("Detokenized response: " + str(response))
    return rides_data

def sp_ext_service_get_flagged_rides(user, context=None):
    
    credentials_path = sp_getCredentials_path(user)
    
    print("credentials_path: " + credentials_path)

    signed_jwt, creds = sp_tokenservice.sp_service_getSignedJWT(credentials_path, context)
    bearer_token, creds = sp_tokenservice.sp_service_getBearerToken(signed_jwt, creds, context)

    query = """
        select * from ride where ride.flagged = true
        """
    
    column_redactions = [
        {"column": "drivephone", "redaction": RedactionType.PLAIN_TEXT},
        {"column": "passengerphone", "redaction": RedactionType.PLAIN_TEXT}
    ]
    
    vault_url = creds["vaultURL"]
    vault_id = creds["vaultID"]
    rides_data = sp_service_query_execute(query, bearer_token, vault_id, vault_url, column_redactions, context)

    #print("rides_data: " + str(rides_data))

    #response = detokenize(rides_data, DetokenizeOptions(continueOnError=True))
    #print("Detokenized response: " + str(response))
    return rides_data


def sp_ext_service_get_flagged_ride_driver_detail(country, rideid):
   try:
        response = ""
        user = ""
        context = None
        if country == "US":
            user = "support"
        else:
            user = "in-support"

        credentials_path = sp_getCredentials_path(user)
        print("credentials_path: " + credentials_path)

        signed_jwt, creds = sp_tokenservice.sp_service_getSignedJWT(credentials_path)
        bearer_token, creds = sp_tokenservice.sp_service_getBearerToken(signed_jwt, creds)
        column_redactions = [
            {"column": "drivephone", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "passengerphone", "redaction": RedactionType.PLAIN_TEXT}
        ]
        query = "select * from ride where ride.flagged=true and ride.rideid=" + str(rideid)
        print(query)

        vault_url = creds["vaultURL"]
        vault_id = creds["vaultID"]
        rides_data = sp_service_query_execute(query, bearer_token, vault_id, vault_url, column_redactions, context)
        #print(rides_data)
        driverid = ""
        for record in rides_data["records"]:
            driverid = record["fields"]["driverid"]
            
        #print(driverid)

        credentials_path = sp_getCredentials_path("")
        print("credentials_path: " + credentials_path)

        signed_jwt, creds = sp_tokenservice.sp_service_getSignedJWT(credentials_path)
        bearer_token, creds = sp_tokenservice.sp_service_getBearerToken(signed_jwt, creds)
        column_redactions = [
            {"column": "fname", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "lname", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "drivers_license_number", "redaction": RedactionType.PLAIN_TEXT}
        ]
        query = "select * from driver where driver.driverid=" + str(driverid)
        print(query)

        vault_url = creds["vaultURL"]
        vault_id = creds["vaultID"]
        driver_data = sp_service_query_execute(query, bearer_token, vault_id, vault_url, column_redactions, context)

        print(driver_data)
        response = driver_data
        return response
   
   except SkyflowError as e:
        print(f"Skyflow Error: {e}")
        raise
   except Exception as e:  
        print(f"Error: {e}")
        raise    

def sp_ext_service_get_flagged_ride_passenger_detail(country, rideid):
   try:
        response = ""
        user = ""
        context = None
        if country == "US":
            user = "support"
        else:
            user = "in-support"

        credentials_path = sp_getCredentials_path(user)
        print("credentials_path: " + credentials_path)

        signed_jwt, creds = sp_tokenservice.sp_service_getSignedJWT(credentials_path)
        bearer_token, creds = sp_tokenservice.sp_service_getBearerToken(signed_jwt, creds)
        column_redactions = [
            {"column": "drivephone", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "passengerphone", "redaction": RedactionType.PLAIN_TEXT}
        ]
        query = "select * from ride where ride.flagged=true and ride.rideid=" + str(rideid)
        #print(query)

        vault_url = creds["vaultURL"]
        vault_id = creds["vaultID"]
        rides_data = sp_service_query_execute(query, bearer_token, vault_id, vault_url, column_redactions, context)
        #print(rides_data)
        passengerid = ""
        for record in rides_data["records"]:
            passengerid = record["fields"]["passengerid"]
            
        #print(passengerid)

        credentials_path = sp_getCredentials_path("")
        print("credentials_path: " + credentials_path)

        signed_jwt, creds = sp_tokenservice.sp_service_getSignedJWT(credentials_path)
        bearer_token, creds = sp_tokenservice.sp_service_getBearerToken(signed_jwt, creds)
        column_redactions = [
            {"column": "fname", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "lname", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "email", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "address", "redaction": RedactionType.PLAIN_TEXT},
            {"column": "phone", "redaction": RedactionType.PLAIN_TEXT}
        ]
        query = "select * from passenger where passenger.passengerid=" + str(passengerid)
        #print(query)

        vault_url = creds["vaultURL"]
        vault_id = creds["vaultID"]
        passenger_data = sp_service_query_execute(query, bearer_token, vault_id, vault_url, column_redactions, context)

        print(passenger_data)
        response = passenger_data
        return response
   
   except SkyflowError as e:
        print(f"Skyflow Error: {e}")
        raise
   except Exception as e:  
        print(f"Error: {e}")
        raise    

def sp_service_query_execute(query, bearer_token, vault_id, vault_url, column_redactions, context=None):
   try:
        # Configure Skyflow Vault client
        config = Configuration(vault_id, vault_url, lambda: bearer_token)
        client = Client(config)
        
        querydata = { 
            "query": query,
            "columnRedactions": column_redactions if column_redactions else []
        }
        # Execute the query
        response = client.query(querydata)#, query_option)
        #print("response: " + str(response))

        #if response and "records" in response:
        #    tokens = [record["fields"].get("drivephone") for record in response["records"] if "drivephone" in record["fields"]]
        #    print("tokens: " + str(tokens))

        #    if tokens:

        #        records = {
        #            "records": [
        #                {"token": token, "redaction": "PLAIN_TEXT"}
        #                for token in tokens
        #            ]
        #        }
        #        print("records: " + str(records))
        #        response = client.detokenize(records, DetokenizeOptions(continueOnError=True))
        #        print("Detokenize Response:", json.dumps(response, indent=2))

        return response
   
   except SkyflowError as e:
        print(f"Skyflow Error: {e}")
        raise
   except Exception as e:  
        print(f"Error: {e}")
        raise    
       
def main():
    try:
        sp_ext_service_get_flagged_ride_driver_detail("US", 10001)
        sp_ext_service_get_flagged_ride_passenger_detail("US", 10001)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()