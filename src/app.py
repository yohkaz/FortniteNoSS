import os
import eel
from fortnite_noss import FortniteNoSS


def init_gui():
    eel.init(r'gui')
    eel.start('main.html', port=0, size=(780, 900))


# Expose FortniteNoSS methods
@eel.expose
def get_all_players():
    with FortniteNoSS() as noss:
        return list(map(lambda p: (p[1], p[0], p[3], p[2]), noss.get_all_players()))

@eel.expose
def reset_database():
    with FortniteNoSS() as noss:
        noss.reset_database()

@eel.expose
def analyze_replays():
    with FortniteNoSS() as noss:
        noss.set_replays_dir(read_replays_dir_path())
        return noss.analyze_replays()

@eel.expose
def add_player(player, info):
    if player is None or player == '':
        return False

    with FortniteNoSS() as noss:
        if info == 'id':
            return noss.add_player_by_id(player.lower())
        elif info == 'username':
            return noss.add_player_by_username(player)

@eel.expose
def reset_player(account_id):
    if account_id is None or account_id == '':
        return False

    with FortniteNoSS() as noss:
        return noss.reset_player(account_id)

@eel.expose
def delete_player(account_id):
    if account_id is None or account_id == '':
        return False

    with FortniteNoSS() as noss:
        return noss.delete_player(account_id)


# Expose replays directory path operations
@eel.expose
def check_directory(dir):
    return os.path.isdir(dir)

@eel.expose
def get_computer_user():
    user = os.getenv('username')
    if user is None:
        return ''
    return user

@eel.expose
def save_replays_dir_path(path):
    with open('replays_dir_path.txt', 'w') as f:
        f.write(path)

@eel.expose
def delete_replays_dir_path():
    try:
        os.remove('replays_dir_path.txt')
    except:
        pass

@eel.expose
def read_replays_dir_path():
    try:
        with open('replays_dir_path.txt', 'r') as f:
            return f.read()
    except:
        return None


if __name__ == "__main__":
    init_gui()