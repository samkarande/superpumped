import json

from skyflow.service_account import is_expired #type : ignore 
from skyflow.service_account import generate_bearer_token # type: ignore
#from skyflow.errors import SkyflowError


# cache token for reuse
superpumped_bearerToken = ''
superpumped_tokenType = ''
def token_provider():

    global superpumped_bearerToken
    global superpumped_tokenType
    if is_expired(superpumped_bearerToken):
        superpumped_bearerToken, superpumped_tokenType = generate_bearer_token('credentials.json')
    return superpumped_bearerToken, superpumped_tokenType

try:
    superpumped_accessToken, superpumped_tokenType = token_provider()
    print("Access Token:", superpumped_accessToken)
    print("Type of token:", superpumped_tokenType)
except SkyflowError as e:
    print(e)