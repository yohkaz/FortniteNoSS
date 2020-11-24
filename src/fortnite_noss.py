import os
import time
import requests

from FortniteReplay import FortniteReplay
from database import Database

class FortniteNoSS:
    def __init__(self):
        self.db = Database(r'./data.db')
        self.replays_dir = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


    def set_replays_dir(self, path):
        self.replays_dir = path


    def reset_database(self):
        self.db.clear_db()


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
        try:
            all_replays = self.db.find_all_replays()

            player_replays = []
            for replay in all_replays:
                if account_id in replay[2]:
                    player_replays.append(replay[0])

            return self.db.create_player(account_id, username, player_replays)
        except:
            return False


    def get_all_players(self):
        try:
            return self.db.find_all_players()
        except:
            return False


    def analyze_replays(self):
        if self.replays_dir is None:
            return False

        try:
            last_replay_file, last_replay_time = self.db.find_last_replay()
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
            #ss_players = self.db.find_all_players_ids()
            ss_players = self.db.find_all_players()
            for file in files:
                self.analyze_replay(file, ss_players)
        except:
            return False

        return True


    def analyze_replay(self, replay_file, ss_players):
        print('Analyzing', replay_file)
        try:
            replay_path = os.path.join(self.replays_dir, replay_file)
            players_ids = FortniteReplay.get_players_ids(replay_path)
            self.db.create_replay(replay_file, os.path.getmtime(replay_path), players_ids)
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
                    self.db.update_player(ss_player[0], username, [replay_file])
                except:
                    return False


    @staticmethod
    def player_username_to_id(username):
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


    @staticmethod
    def player_id_to_username(account_id):
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

