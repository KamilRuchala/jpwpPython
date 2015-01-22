import json, requests

url = 'http://192.168.0.16:8888'

params = dict(
    address='localhost',
    port='0',
    type='text',
    content='country(russia)'
)

resp = requests.get(url=url, params=params)
print resp.text
