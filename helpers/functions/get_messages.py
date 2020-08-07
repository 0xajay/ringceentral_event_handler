import requests
import os
from helpers.functions.get_ringcentral_access_token import get_ringcentral_access_token


accountID = os.environ.get('ACCOUNT_ID')
extensionID = os.environ.get('EXTENSION_ID')
server_url = os.environ.get('RINGCENTRAL_SERVER_URL')

def get_messages():
    try:
        url = server_url+"/restapi/v1.0/account/"+accountID+"/extension/"+extensionID+"/message-store"
        token = get_ringcentral_access_token()
        headers = {"Authorization": "Bearer "+token}
        result = requests.get(url, headers=headers).json()
        # print(result)
        result = sorted(result['records'], key=lambda k: k['id'])
        return result, token

    except Exception as err:
        print(err)
