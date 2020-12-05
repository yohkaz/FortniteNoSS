import os
import subprocess
import json

class FortniteReplay:
    def __init__(self):
        self.replays_dir = self.read_replays_dir()
        if self.replays_dir is None:
            self.set_default_replays_dir()


    def set_replays_dir(self, path):
        if self.check_directory(path):
            self.replays_dir = path
            self.save_replays_dir()
            return True
        else:
            self.replays_dir = None
            self.delete_replays_dir()
            return False


    def set_default_replays_dir(self):
        computer_user = os.getenv('username')
        if computer_user is None:
            return False

        default_replays_dir = "C:\\Users\\" + computer_user + "\\AppData\\Local\\FortniteGame\\Saved\\Demos"
        return self.set_replays_dir(default_replays_dir)


    def get_replays_dir(self):
        return self.replays_dir


    def save_replays_dir(self):
        if self.replays_dir is None:
            return

        with open('replays_dir_path.txt', 'w') as f:
            f.write(self.replays_dir)


    def delete_replays_dir(self):
        try:
            os.remove('replays_dir_path.txt')
        except:
            pass


    def read_replays_dir(self):
        try:
            with open('replays_dir_path.txt', 'r') as f:
                return f.read()
        except:
            return None


    def get_replay_data(self, replay_path):
        if replay_path is None:
            return None

        dotnet_exe_path = os.path.join('FortniteReplay.exe')

        # Run external cmd without console popup
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen([dotnet_exe_path, replay_path], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = process.stdout.read().decode('utf-8')

        # TODO: Check if this catch analyzing a replay not completed (while still in game)
        error = process.stderr.read().decode('utf-8')
        if error:
            raise RuntimeError('FortniteReplay: ' + error)

        replay_data = json.loads(output)
        replay_data['filename'] = os.path.basename(replay_path)
        return replay_data

    @staticmethod
    def extract_players_ids(replay_data):
        players = replay_data['players']
        players_ids = [p['PlayerId'] for p in players]
        players_ids = list(map(lambda x: x.lower(), players_ids))
        return players_ids

    @staticmethod
    def extract_players(replay_data):
        players_by_id = {}
        players_data = replay_data['players']
        for player in players_data:
            player['PlayerId'] = player['PlayerId'].lower()
            player['Platform'] = player['Platform'].lower()
            players_by_id[player['PlayerId']] = player

        return players_by_id

    @staticmethod
    def extract_killfeed(replay_data):
        killfeed = replay_data['killfeed']
        killfeed_arr = []

        for kf in killfeed:
            kf_dict = {}

            # Killer info
            kf_dict['EliminatorID'] = kf['Eliminator'].lower()
            # Killed info
            kf_dict['EliminatedID'] = kf['Eliminated'].lower()
            # Action info
            if kf['Knocked'] == 'true':
                kf_dict['Action'] = "Knocked"
            else:
                kf_dict['Action'] = "Killed"
            # Time info
            kf_dict['Time'] = kf['Time']
            killfeed_arr.append(kf_dict)

        return killfeed_arr

    @staticmethod
    def check_directory(dir):
        return os.path.isdir(dir)