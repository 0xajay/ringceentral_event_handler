import requests
import os

accountID = os.environ.get('ACCOUNT_ID')
extensionID = os.environ.get('EXTENSION_ID')
server_url = os.environ.get('RINGCENTRAL_SERVER_URL')

def get_call_logs(token):
    try:
        url = server_url+"/restapi/v1.0/account/"+accountID+"/extension/"+extensionID+"/call-log?showBlocked=true&view=Detailed&withRecording=false&page=1&perPage=100&showDeleted=false"
        headers = {"Authorization": "Bearer "+token}
        result = requests.get(url, headers=headers).json()
        result = sorted(result['records'], key=lambda k: k['sessionId'])
        return result
    except Exception as err:
        print(err)
