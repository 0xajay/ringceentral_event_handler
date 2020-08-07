import requests

def create_call_engagement(contact_id,log_date,call_type, receiver_name, receiver_phone, sender_name,sender_phone, duration, owner_id):

    url = "https://api.hubapi.com/engagements/v1/engagements?hapikey=145f865d-2dc3-465b-a822-6f6f92186511"
    payload = {
    "engagement": {
        "active": True,
        "ownerId": owner_id,
        "type": "CALL"
    },
    "associations": {
        "contactIds": [contact_id],
        "companyIds": [ ],
        "dealIds": [ ],
        "ownerIds": [ ],
		"ticketIds":[ ]
    },
    "metadata": {
        "toNumber":receiver_name + " +1 "+receiver_phone,
        "fromNumber":"+1 "+sender_phone,
        "status":"COMPLETED",
        "durationMilliseconds":duration,
        "body": log_date+": ["+call_type+"] CALL from <b>"+sender_name+"</b> ("+sender_phone+") to <b>"+receiver_name+"</b> ("+receiver_phone+")"
    }
    }
    result = requests.post(url, json=payload).json()
    print(result,"call log")
