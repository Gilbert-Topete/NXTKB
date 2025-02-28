import requests
import requests.auth
from hidden_vars import *
import base64

def base64encode(username, password):
    str_key = "{username}:{password}"
    byte_key = str_key.encode('ascii')
    b64_key = "Basic " + str(base64.b64encode(byte_key))
    return b64_key

service_tickets_url = "https://na.myconnectwise.net/v4_6_release/apis/3.0/service/ticketLinks"
username = COMPANY_ID + PUBLIC_KEY
password = PRIVATE_KEY

auth_key = base64encode(username, password)

headers = {
    'Authorization': auth_key,
    'clientId': CW_CLIENTID
    }

response = requests.request("GET", service_tickets_url, headers=headers)

print(response.text)