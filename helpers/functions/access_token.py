import requests

def get_access_token():
    try:
        with open("helpers/functions/token.txt","r") as f:
            refresh_token = f.read()
        url = "https://api.hubapi.com/oauth/v1/token"
        data = {
            "grant_type":"refresh_token",
            "client_id":"a950cc9b-c054-4f8e-adb1-a0d4476f950b",
            "client_secret":"fbd8261f-6bca-4fe7-badd-8098a4948aeb",
            "refresh_token":refresh_token.replace('\n','')
        }
        result = requests.post(url, data=data).json()
        print(result)
        with open("helpers/functions/token.txt","w") as g:
            g.write(result["refresh_token"])
        return result["access_token"]

    except Exception as err:
        print(err)
