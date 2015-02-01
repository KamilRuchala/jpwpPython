import json, requests
# http://www.33ff.com/flags/L_flags/Turkey_flags.gif

url = "http://localhost:8888"
#data = {'address': 'localhost', 'port': '9999', 'type': 'text', 'content': 'country(poland);getflag'}
data = {'address': 'localhost', 'port': '9999', 'type': 'text', 'content': 'checkflag(http://www.33ff.com/flags/L_flags/Chile_flags.gif)'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print r.text
