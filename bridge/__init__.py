import os, base64, json
#from urllib.request import Request, urlopen
#from urllib.parse import urlencode
import requests

def make_request(url=None, data=None, headers=None):
    request_headers = {
        **headers,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url=url, json=data, headers=request_headers) if data else requests.get(url=url, headers=request_headers)
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        message = 'an unknown error occurred.'
        return { 'error': message }



base_uri = 'http://localhost:5000/api'

eml = os.environ.get('H2H_ADMIN_USERNAME')
pwd = os.environ.get('H2H_ADMIN_PWD')

auth_string = bytes(eml + ':' + pwd, 'utf-8')
basic_header = { 'Authorization': 'Basic ' + base64.b64encode(auth_string).decode() }
auth_data = make_request(url=base_uri+'/auth/login', headers=basic_header)
token_header = { 'Authorization': 'Bearer ' + auth_data['data']['token'] }


    



