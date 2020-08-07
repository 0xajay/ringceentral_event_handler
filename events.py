import requests
import time
from datetime import datetime
import random, string
import base64
import os
from helpers.functions.timeline_events import create_received_timeline, create_sent_timeline
from helpers.functions.get_messages import get_messages
# from helpers.functions.get_devices import get_devices
from datetime import datetime
from helpers.functions.create_call_engagement import create_call_engagement
from helpers.functions.get_call_logs import get_call_logs
from helpers.functions.format_phone_number import format_phone_number
from pytz import timezone, utc

with open("counter.txt", "r") as f:
    counter = f.readlines()[0]

with open("call_counter.txt","r") as g:
    call_counter = g.readlines()[0]

while True:
    start_time = time.time()
    result,token = get_messages()
    # device_list = get_devices(token)
    call_logs = get_call_logs(token)
    for msg in result:
        if msg["id"] > int(counter):
            if msg["direction"] == "Inbound":
                sender = requests.get("https://api.hubapi.com/contacts/v1/search/query?q="+(msg['from']['phoneNumber']).replace('+1','')+"&hapikey=145f865d-2dc3-465b-a822-6f6f92186511").json()
                sender_name = sender["contacts"][0]["properties"]["firstname"]["value"] + " "+ sender["contacts"][0]["properties"]["lastname"]["value"]
                identities = sender["contacts"][0]["identity-profiles"][0]["identities"]
                email = ''
                for i in identities:
                    if i['type'] == "EMAIL":
                        email = i["value"]
                receiver_phone = msg['to'][0]['phoneNumber']
                receiver_name = msg['to'][0]['name']
                sender_phone = msg['from']['phoneNumber']
                message = (msg['subject'].split('-'))[1]
                # print("Sent by "+sender_name+" ("+sender_phone+") to Hubspot User: "+receiver_name+" ("+receiver_phone+")<br/><br/>Message: "+message)
                create_received_timeline(sender_phone,message,email,sender_name,receiver_name,receiver_phone)
                counter = msg["id"]
                with open("counter.txt","w") as g:
                    g.write(str(msg["id"]))

            if msg["direction"] == "Outbound":

                receiver = requests.get("https://api.hubapi.com/contacts/v1/search/query?q="+(msg['to'][0]["phoneNumber"]).replace('+1','')+"&hapikey=145f865d-2dc3-465b-a822-6f6f92186511").json()
                print(receiver)
                receiver_contact_id = receiver["contacts"][0]["vid"]
                receiver_name = receiver["contacts"][0]["properties"]["firstname"]["value"] + " "+ receiver["contacts"][0]["properties"]["lastname"]["value"]
                email = receiver["contacts"][0]["properties"]["email"]["value"]
                sender_phone = msg["from"]["phoneNumber"]
                sender_name = msg["from"]["name"]
                receiver_phone = msg['to'][0]["phoneNumber"]
                message = (msg['subject'].split('-'))[1]
                create_sent_timeline(receiver_phone,message,email, receiver_name, sender_name, sender_phone)
                counter = msg["id"]
                with open("counter.txt","w") as g:
                    g.write(str(msg["id"]))

    for call in call_logs:
        if int(call["sessionId"]) > int(call_counter):
            if call["direction"] == "Outbound":
                date = datetime.strptime(call["lastModifiedTime"],"%Y-%m-%dT%H:%M:%S.%fZ")
                eastern = timezone('US/Eastern')
                date = date.replace(tzinfo=utc).astimezone(eastern)
                log_date = date.strftime('%b')+" "+date.strftime('%d')+", "+date.strftime("%Y")+" "+date.strftime("%I")+":"+date.strftime("%M")+" "+date.strftime("%p")
                call_type = call["direction"] + " "+ call["result"]
                sender_name = call["from"]["name"]
                if 'phoneNumber' in call["from"]:
                    sender_phone = format_phone_number(call["from"]["phoneNumber"])
                    receiver_phone = format_phone_number(call["to"]["phoneNumber"])
                    receiver = requests.get("https://api.hubapi.com/contacts/v1/search/query?q="+(receiver_phone.replace('+1',''))+"&hapikey=145f865d-2dc3-465b-a822-6f6f92186511").json()
                    contact_id = receiver["contacts"][0]["vid"]
                    receiver_name = receiver["contacts"][0]["properties"]["firstname"]["value"] + " "+ receiver["contacts"][0]["properties"]["lastname"]["value"]
                    duration = int(call["duration"]) * 1000
                    owner_id = receiver["contacts"][0]["properties"]["hubspot_owner_id"]["value"]
                    create_call_engagement(contact_id, log_date, call_type, receiver_name, receiver_phone, sender_name, sender_phone, duration,owner_id)
                    call_counter = call["sessionId"]
                    with open("call_counter.txt","w") as g:
                        g.write(str(call["sessionId"]))

            if call["direction"] == "Inbound":
                date = datetime.strptime(call["lastModifiedTime"],"%Y-%m-%dT%H:%M:%S.%fZ")
                eastern = timezone('US/Eastern')
                date = date.replace(tzinfo=utc).astimezone(eastern)
                log_date = date.strftime('%b')+" "+date.strftime('%d')+", "+date.strftime("%Y")+" "+date.strftime("%I")+":"+date.strftime("%M")+" "+date.strftime("%p")
                call_type = call["direction"] + " "+ call["result"]
                receiver_name = call["to"]["name"]
                if 'phoneNumber' in call['from']:
                    sender_phone = format_phone_number(call["from"]["phoneNumber"])
                    receiver_phone = format_phone_number(call["to"]["phoneNumber"])
                    sender = requests.get("https://api.hubapi.com/contacts/v1/search/query?q="+(sender_phone.replace('+1',''))+"&hapikey=145f865d-2dc3-465b-a822-6f6f92186511").json()
                    contact_id = sender["contacts"][0]["vid"]
                    sender_name = sender["contacts"][0]["properties"]["firstname"]["value"] + " "+ sender["contacts"][0]["properties"]["lastname"]["value"]
                    duration = int(call["duration"]) * 1000
                    owner_id = sender["contacts"][0]["properties"]["hubspot_owner_id"]["value"]
                    create_call_engagement(contact_id, log_date, call_type, receiver_name, receiver_phone, sender_name, sender_phone, duration, owner_id)
                    call_counter = call["sessionId"]
                    with open("call_counter.txt","w") as g:
                        g.write(str(call["sessionId"]))

    print("\n\n--- %s seconds ---" % (time.time() - start_time))

    time.sleep(30)
