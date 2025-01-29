import requests
import os
import json
import urllib.parse

baseDir = os.path.join(os.getcwd(),"Data")
print(baseDir)
def txtFileDict(filename, phone, password=None, access_token=None, refresh_token=None):
    array = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            array = json.load(file)
    if password != None:
        account = {
            'phone': phone,
            'password': password
        }
    else:
        account = {
            'phone': phone,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    first_key = next(iter(account))
    for i, obj in enumerate(array):
        if obj[first_key] == account[first_key]:
            array[i] = account
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(array, file, indent=4)
            return
    array.append(account)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(array, file, indent=2)
def login_by_password(phone, password):
    url = 'https://api.gsm-api.net/auth/v1/public/user/login?aud=user_app&platform=android'
    payload = {
        "phone": phone,
        "password": password
    }
    headers = {
        "platform": "android",
        "aud": "user_app",
        "content-type": "application/json; charset=UTF-8"
    }
    r = requests.post(url, json=payload, headers=headers)
    print(r.json())
    if r.status_code == 200:
        data = r.json()['data']
        txtFileDict(os.path.join(baseDir,"AccountToken.json"),phone=data['phone'], access_token=data['access_token'], refresh_token=data['refresh_token'])
        return data['access_token']
def search_location_pickup(text, token):
    url = f'https://api.gsm-api.net/maps/v1/public/place/autocomplete?text={urllib.parse.quote(text)}&search_location=pickup&country_code=VNM'
    headers = {
        "platform": "android",
        "aud": "user_app",
        "authorization": f"Bearer {token}"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()['data']
        list_data = []
        for index, data in enumerate(data):
            print(index, data['label'])
            list_data.append(data)
        return list_data
login_by_password("+84396325164","779321")
# search_location_pickup("133/48/15 Quang Trung Phuong 10 Quan Go Vap",)