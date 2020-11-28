import os
import eel
from fortnite_noss import FortniteNoSS

noss = FortniteNoSS()

def init_gui():
    #noss.fortnitewebapi_set_auth_code('0e72e777ad574397b5c322c7b86705c5')
    eel.init(r'gui')
    eel.start('about.html', port=0, size=(780, 900))


# Expose FortniteNoSS methods
@eel.expose
def get_all_players():
    return list(map(lambda p: (p[1], p[0], p[3], p[2]), noss.get_all_players()))

@eel.expose
def reset_database():
    noss.reset_database()

@eel.expose
def analyze_replays():
    return noss.analyze_replays()

@eel.expose
def number_analyzed_replays():
    number = noss.get_analyzed_replays()
    if number is None:
        return -1
    return len(number)

@eel.expose
def number_new_replays():
    number = len(noss.get_new_replays())
    if number is None:
        return 0
    return number

@eel.expose
def add_player(player, info):
    if player is None or player == '':
        return False

    if info == 'id':
        return noss.add_player_by_id(player.lower())
    elif info == 'username':
        return noss.add_player_by_username(player)

@eel.expose
def reset_player(account_id):
    if account_id is None or account_id == '':
        return False

    return noss.reset_player(account_id)

@eel.expose
def delete_player(account_id):
    if account_id is None or account_id == '':
        return False

    return noss.delete_player(account_id)

# Expose FortniteWebAPI methods
@eel.expose
def fortnitewebapi_status():
    return noss.fortnitewebapi_status()


@eel.expose
def fortnitewebapi_set_auth_code(auth_code):
    return noss.fortnitewebapi_set_auth_code(auth_code)

@eel.expose
def fortnitewebapi_clear_auth():
    return noss.reset_auth()

@eel.expose
def fortnitewebapi_session_username():
    return noss.fortnitewebapi_session_username()


# Expose replays directory path methods
@eel.expose
def set_replays_dir(path):
    return noss.set_replays_dir(path)

@eel.expose
def set_default_replays_dir():
    return noss.set_default_replays_dir()

@eel.expose
def get_replays_dir():
    return noss.get_replays_dir()


if __name__ == "__main__":
    init_gui()