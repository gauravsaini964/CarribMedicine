import requests
import json
def req():
    url = "https://lmsapi.tis.edu.in/lead/create/outside"

    # payload = "{\n    \"name\": \"jsncsjn\",\n    \"phones\": \"9876543210\",\n    \"email\": \"jnas@nbds.com\"\n}"
    payload = {
        "name": "Gaurav",
        "phones": "9999924722",
        "email": "gauravsaini22222@gmail.com"
    }
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "5631623e-0500-4f84-a76d-fb9c80be74c5"
        }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    print(response.text)

req()


