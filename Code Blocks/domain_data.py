import requests
import json

client_id = 'client_ceee15955e8315318fafc2357c4d928c'
client_secret = 'secret_1afa96b175a161d582804fed5669d703'
scopes = ['api_properties_read']
auth_url = 'https://auth.domain.com.au/v1/connect/token'
url_endpoint = 'https://api.domain.com.au/v1/salesResults/_head'
property_id = 'RF-8884-AK'


def get_property_info():
    response = requests.post(auth_url, data = {
                        'client_id':client_id,
                        'client_secret':client_secret,
                        'grant_type':'client_credentials',
                        'scope':scopes,
                        'Content-Type':'text/json'
                        })
    json_res = response.json()
    access_token=json_res['access_token']
    print(access_token)
    auth = {'Authorization':'Bearer ' + access_token}
    url = url_endpoint + property_id
    res1 = requests.get(url, headers=auth)    
    r = res1.json()
    print(r)


get_property_info()

