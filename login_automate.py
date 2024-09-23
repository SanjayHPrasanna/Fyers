

# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel
import credentials as cd
import pyotp as tp
client_id = cd.client_id
secret_key = cd.secret_key
redirect_uri =cd.redirect_uri
user_name=cd.user_name
totp_key=cd.totp_key
# pin1 =cd.pin1
# pin2 = cd.pin2
# pin3 = cd.pin3
# pin4 = cd.pin4


# Replace these values with your actual API credentials

response_type = "code"  
state = "sample_state"

# Create a session model with the provided credentials
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)

# Generate the auth code using the session model
response = session.generate_authcode()

# Print the auth code received in the response
print(response)


link=response

totp_key = 'QMFSLXH7C5Z4C7HL2OZCXWX6Q75FVDVL'
k=tp.TOTP(totp_key).now()
print (k)




