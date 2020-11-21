import requests

url = "https://notify-api.line.me/api/notify"
token = "wdviMOdjmcYW1cTNfMqDTNlq2Fheh8qQlNDTMWS2EA2"
headers = {'Authorization':'Bearer ' + token}

msg = {
    "message": "Line Notify from Kita's Raspberry Pi"
    }

files = {'imageFile': open('perth.png', 'rb')}

res = requests.post(url, headers=headers, data=msg, files=files)
print (res.text)