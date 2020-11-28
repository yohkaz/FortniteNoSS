import os
import subprocess

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


    def get_players_ids(self, replay_path):
        if replay_path is None:
            return None

        dotnet_exe_path = os.path.join('FortniteReplay.exe')

        # Run external cmd without console popup
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen([dotnet_exe_path, replay_path], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = process.stdout.read().decode('utf-8')

        #output = subprocess.check_output([dotnet_exe_path, replay_path], shell=True).decode('utf-8')
        list_of_player_ids = output.split(',')[:-1]
        list_of_player_ids = list(map(lambda x: x.lower(), list_of_player_ids))
        return list_of_player_ids


    @staticmethod
    def check_directory(dir):
        return os.path.isdir(dir)