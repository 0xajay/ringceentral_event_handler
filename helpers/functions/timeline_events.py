import requests
from helpers.functions.access_token import get_access_token
import random, string

def create_received_timeline(phone, message, email, name, receiver_name, receiver_phone):
    try:
        endpoint = "https://api.hubapi.com/integrations/v1/222358/timeline/event"
        data = {
        "id": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
        "eventTypeId": 1005844,
        "sms_name": name,
        "sms_phone":phone,
        "sms_body": message,
        "receiver_name":receiver_name,
        "receiver_phone":receiver_phone,
        "email": email
        }
        access_token = get_access_token()
        headers = {"Authorization": "Bearer "+access_token}
        result = requests.put(endpoint, json=data, headers=headers).json()
        print(result)
    except Exception as err:
        print(err)

def create_sent_timeline(phone, message, email, name, sender_name, sender_phone):
    try:
        endpoint = "https://api.hubapi.com/integrations/v1/222358/timeline/event"
        data = {
        "id": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
        "eventTypeId": 1005680,
        "sms_name": name,
        "sms_phone":phone,
        "sms_body": message,
        "sender_name":sender_name,
        "sender_phone":sender_phone,
        "email": email
        }
        access_token = get_access_token()
        headers = {"Authorization": "Bearer "+access_token}
        result = requests.put(endpoint, json=data, headers=headers)
        print(result)
    except Exception as err:
        print(err)
