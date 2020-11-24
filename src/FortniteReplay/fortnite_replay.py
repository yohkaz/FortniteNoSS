import os
import subprocess

class FortniteReplay:
    @staticmethod
    def get_players_ids(replay_path):
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
