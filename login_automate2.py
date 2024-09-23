# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel
import credentials as cd
import pyotp as tp
client_id = cd.client_id
secret_key = cd.secret_key
redirect_uri =cd.redirect_uri
user_name=cd.user_name
totp_key=cd.totp_key
auth_code=cd.auth_code

response_type = "code" 
grant_type = "authorization_code"  


# Create a session object to handle the Fyers API authentication and token generation
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)

# Set the authorization code in the session object
session.set_token(auth_code)

# Generate the access token using the authorization code
response = session.generate_token()


access_token=response['access_token']
with open('access.txt','w') as k:
    k.write(access_token)

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

response = fyers.holdings()
response2=fyers.get_profile()
print(response)
print(response2)