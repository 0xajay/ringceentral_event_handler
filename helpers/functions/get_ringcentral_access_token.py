import requests
import os
import base64

accountID = os.environ.get('ACCOUNT_ID')
extensionID = os.environ.get('EXTENSION_ID')
server_url = os.environ.get('RINGCENTRAL_SERVER_URL')
client_id = os.environ.get("RINGCENTRAL_CLIENT_ID")
client_secret = os.environ.get("RINGCENTRAL_CLIENT_SECRET")

code = client_id+":"+client_secret

authorization_code = base64.b64encode(code.encode('ascii'))


def get_ringcentral_access_token():
    try:
        a_url =server_url+"/restapi/oauth/token"
        a_header = {"Authorization": "Basic "+authorization_code.decode('ascii')}
        payload = {
            'grant_type':'password',
            'username':os.environ.get('RINGCENTRAL_USERNAME'),
            'password':os.environ.get('RINGCENTRAL_PASSWORD'),
            'extension':os.environ.get('RINGCENTRAL_EXTENSION')
        }

        token = requests.post(a_url, data=payload, headers=a_header).json()
        return token['access_token']
    except Exception as err:
        print(err)
