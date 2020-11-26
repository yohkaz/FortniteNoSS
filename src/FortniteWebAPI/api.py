import os
import json
import requests
from datetime import datetime, timedelta
from . import endpoints


class FortniteWebAPI():
    def __init__(self):
        self.launcher_token = 'MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE'
        self.fortnite_token = 'ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ'
        self.device_info_filename = 'device_info.json'
        self.session = None

    def auth(self):
        return self.device_auth()

    def auth_status(self):
        return self.session is not None

    def device_auth(self):
        print('FortniteWebAPI: Device Auth')

        device_info = self.get_device_auth_info()
        if device_info is None:
            return False

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'basic {}'.format(self.launcher_token),
        }
        data = {
            'grant_type': 'device_auth',
            'device_id': device_info['deviceId'],
            'account_id': device_info['accountId'],
            'secret': device_info['secret']
        }
        try:
            response_token = Session.post_noauth(endpoints.token, headers=headers, data=data)
            response_token_dict = response_token.json()
        except:
            return False
        print('FortniteWebAPI: Token :', response_token_dict)

        self.session = Session(response_token_dict['displayName'],
                               response_token_dict['access_token'],
                               response_token_dict['refresh_token'],
                               response_token_dict['expires_at'],
                               self.fortnite_token)
        return True

    def get_device_auth_info(self):
        if os.path.isfile(self.device_info_filename):
            with open(self.device_info_filename, 'r') as fp:
                return json.load(fp)
        print('FortniteWebAPI: No device_info.json file')
        return None

    def store_device_auth_info(self, device_info):
        with open(self.device_info_filename, 'w') as fp:
            json.dump(device_info, fp)

    def clear_device_auth_info(self):
        os.remove(self.device_info_filename)
        self.session = None

    def generate_device_auth(self, auth_code):
        # Step1: csrf
        try:
            response_csrf = Session.get_noauth(endpoints.csrf)
            xsrf_token = response_csrf.cookies.get_dict()['XSRF-TOKEN']
        except:
            return False
        print(xsrf_token)

        # Step2: token
        headers = {
            'x-xsrf-token': xsrf_token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'basic {}'.format(self.launcher_token),
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'includePerms': True,
            'token_type': 'eg1',
        }
        try:
            response_token = Session.post_noauth(endpoints.token, headers=headers, data=data)
            print('Response token:', response_token)
            print(response_token.json())
            response_token_dict = response_token.json()
            account_id = response_token_dict['account_id']
            access_token = response_token_dict['access_token']
        except:
            return False

        # Step3: device
        headers = {
            'Authorization': 'bearer {}'.format(access_token),
        }
        try:
            response_device = Session.post_noauth(endpoints.device.format(account_id), headers=headers)
            print(response_device)
            print(response_device.json())
        except:
            return False
    
        self.store_device_auth_info(response_device.json())
        return True

    def session_username(self):
        if self.session is None:
            return None

        return self.session.username

    def player_by_username(self, username):
        try:
            response = self.session.get(endpoints.account_by_name.format(username))
            return response.get('id')
        except:
            return None

    def player_by_id(self, account_id):
        try:
            response = self.session.get(endpoints.account_by_id.format(account_id))
            return response.get('displayName')
        except:
            return None


class Session:
    def __init__(self, username, access_token, refresh_token, expires_at, fortnite_token):
        self.username = username
        self.refresh_token = refresh_token
        self.expires_at = self.convert_iso_time(expires_at)
        self.fortnite_token = fortnite_token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'bearer {}'.format(access_token)})

    # Check if the access token needs to be updated
    def check_token(self):
        now = datetime.utcnow()
        if self.expires_at < (now - timedelta(seconds=60)):
            print('FortniteWebAPI: Token Refresh')
            self.refresh()

    def refresh(self):
        response = requests.post(endpoints.token, headers={'Authorization': 'basic {}'.format(self.fortnite_token)},
                                 data={'grant_type': 'refresh_token', 'refresh_token': '{}'.format(self.refresh_token),
                                       'includePerms': True}).json()
        access_token = response.get('access_token')
        self.session.headers.update({'Authorization': 'bearer {}'.format(access_token)})
        self.refresh_token = response.get('refresh_token')
        self.expires_at = self.convert_iso_time(response.get('expires_at'))

    def get(self, endpoint, params=None, headers=None):
        self.check_token()
        response = self.session.get(endpoint, params=params, headers=headers)
        print(response.text)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    def post(self, endpoint, params=None, headers=None):
        self.check_token()
        response = self.session.post(endpoint, params=params, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    @staticmethod
    def get_noauth(endpoint, params=None, headers=None, data=None):
        response = requests.get(endpoint, params=params, headers=headers, data=data)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    @staticmethod
    def post_noauth(endpoint, params=None, headers=None, data=None):
        response = requests.post(endpoint, params=params, headers=headers, data=data)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    @staticmethod
    def convert_iso_time(isotime):
        """Will convert an isotime (string) to datetime.datetime"""
        return datetime.strptime(isotime, '%Y-%m-%dT%H:%M:%S.%fZ')

