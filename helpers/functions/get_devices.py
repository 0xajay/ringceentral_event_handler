import requests
import os

accountID = os.environ.get('ACCOUNT_ID')
extensionID = os.environ.get('EXTENSION_ID')
server_url = os.environ.get('RINGCENTRAL_SERVER_URL')

def get_devices(token):
    try:
        url = server_url+"/restapi/v1.0/account/"+accountID+"/extension/"+extensionID+"/device"
        headers = {"Authorization": "Bearer "+token}
        result = requests.get(url, headers=headers).json()
        device_lists = []
        for device in result["records"]:
            if device["type"] == "SoftPhone":
                device_lists.append(device["id"])
        return device_lists
    except Exception as err:
        print(err)
