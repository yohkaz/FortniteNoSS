import os
import time
import requests

from FortniteWebAPI import FortniteWebAPI
from FortniteReplay import FortniteReplay
from database import Database

class FortniteNoSS:
    def __init__(self):
        self.db_filename = r'./data.db'
        self.replays_dir = None
        self.fortnitewebapi  = FortniteWebAPI()
        self.fortnitewebapi.auth()


    def set_replays_dir(self, path):
        self.replays_dir = path


    def fortnitewebapi_status(self):
        return self.fortnitewebapi.auth_status()


    def fortnitewebapi_set_auth_code(self, auth_code):
        if not self.fortnitewebapi.generate_device_auth(auth_code):
            return False

        return self.fortnitewebapi.auth()


    def fortnitewebapi_session_username(self):
        return self.fortnitewebapi.session_username()


    def reset_database(self):
        with Database(self.db_filename) as db:
            db.clear_db()


    def reset_auth(self):
        self.fortnitewebapi.clear_device_auth_info()


    def add_player_by_id(self, account_id):
        username = self.player_id_to_username(account_id)
        if username is None:
            print('Can\'t find player ', account_id)
            return False

        return self.add_player(account_id, username)


    def add_player_by_username(self, username):
        account_id = self.player_username_to_id(username)
        if account_id is None:
            print('Can\'t find player ', username)
            return False

        return self.add_player(account_id, username)


    def add_player(self, account_id, username):
        with Database(self.db_filename) as db:
            try:
                all_replays = db.find_all_replays()

                player_replays = []
                for replay in all_replays:
                    if account_id in replay[2]:
                        player_replays.append(replay[0])

                return db.create_player(account_id, username, player_replays)
            except:
                return False


    def reset_player(self, account_id):
        with Database(self.db_filename) as db:
            try:
                return db.reset_player(account_id)
            except:
                return False


    def delete_player(self, account_id):
        with Database(self.db_filename) as db:
            try:
                return db.delete_player(account_id)
            except:
                return False


    def get_all_players(self):
        with Database(self.db_filename) as db:
            try:
                return db.find_all_players()
            except:
                return False


    def analyze_replays(self):
        if self.replays_dir is None:
            return False

        with Database(self.db_filename) as db:
            try:
                last_replay_file, last_replay_time = db.find_last_replay()
            except:
                return False

            files = os.listdir(self.replays_dir)
            # Filter out non replay files
            files = list(filter(lambda x: x.endswith('.replay'), files))
            # Filter out already analyzed replays
            if last_replay_file:
                files = list(filter(lambda x: os.path.getmtime(os.path.join(self.replays_dir, x)) > last_replay_time, files))
            # Sort replays from older to newer
            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.replays_dir, x)))

            # Analyze each replay
            try:
                #ss_players = db.find_all_players_ids()
                ss_players = db.find_all_players()
                for file in files:
                    self.analyze_replay(self.replays_dir, file, ss_players, db)
            except:
                return False

            return True


    @staticmethod
    def analyze_replay(replays_dir, replay_file, ss_players, db):
        print('FortniteNoSS: Analyzing', replay_file)
        try:
            replay_path = os.path.join(replays_dir, replay_file)
            players_ids = FortniteReplay.get_players_ids(replay_path)
            db.create_replay(replay_file, os.path.getmtime(replay_path), players_ids)
        except:
            return False

        # Check if stream snipers players are in this replay
        for ss_player in ss_players:
            if ss_player[0] in players_ids:
                # TODO: convert again id to username in case player changed his username
                #       currently too demanding to the fortnite-api service
                #username = self.player_id_to_username(ss_player)
                #if username is None:
                #    return False

                username = ss_player[1]
                try:
                    db.update_player(ss_player[0], username, [replay_file])
                except:
                    return False


    def player_username_to_id(self, username):
        if self.fortnitewebapi.auth_status():
            return self.fortnitewebapi.player_by_username(username)

        endpoint = r'https://fortnite-api.com/v1/stats/br/v2?name=' + username

        # Send request 5 times
        for i in range(5):
            response = requests.get(endpoint)
            if response.status_code == 200:
                break
            elif response.status_code == 503:
                time.sleep(1)
                continue
            else:
                try:
                    response.raise_for_status()
                except requests.HTTPError as e:
                    print(e)
                    print(response.text)
                    return None

        return response.json()['data']['account']['id']


    def player_id_to_username(self, account_id):
        if self.fortnitewebapi.auth_status():
            return self.fortnitewebapi.player_by_id(account_id)

        endpoint = r'https://fortnite-api.com/v1/stats/br/v2/' + account_id

        # Send request 5 times
        for i in range(5):
            response = requests.get(endpoint)
            if response.status_code == 200:
                break
            elif response.status_code == 503:
                time.sleep(1)
                continue
            else:
                try:
                    response.raise_for_status()
                except requests.HTTPError as e:
                    print(e)
                    print(response.text)
                    return None

        return response.json()['data']['account']['name']

    @staticmethod
    def get_exchange_code():
        endpoint = r'https://www.epicgames.com/id/api/redirect?clientId=3446cd72694c4a4485d81b77adbb2141&responseType=code'
        response = requests.get(endpoint)
        print(response.text)


