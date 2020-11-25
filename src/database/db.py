import os
import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = None
        self.create_connection()


    def create_connection(self):
        """ Create a database connection to a SQLite database """
        try:
            self.db = sqlite3.connect('file:' + self.db_file + '?mode=rw', uri=True)
            self.db.set_trace_callback(print)
            print('Succesfully connected to', self.db_file)
        except sqlite3.OperationalError as e:
            print('Database', self.db_file, 'does not exits')
            self.create_db()
        except sqlite3.Error as e:
            print(e)


    def create_db(self):
        """ Create a new SQLite database """
        try:
            print('Create SQLite database', self.db_file)
            self.db = sqlite3.connect(self.db_file)
            self.db.set_trace_callback(print)

            players_table = """
                                CREATE TABLE IF NOT EXISTS players (
                                    account_id text PRIMARY KEY,
                                    username text NOT NULL,
                                    replay_files text NOT NULL,
                                    counter integer NOT NULL
                                )
                              """
            self.create_table(players_table)

            replays_table = """
                                CREATE TABLE IF NOT EXISTS replays (
                                    replay_file text PRIMARY KEY,
                                    time REAL NOT NULL,
                                    players_ids text NOT NULL
                                )
                              """
            self.create_table(replays_table)
        except sqlite3.Error as e:
            print('Could not create database', self.db_file)
            print(e)
            raise RuntimeError('db.py: create_db()') from e


    def clear_db(self):
        self.close()
        os.remove(self.db_file)
        self.create_db()


    def create_table(self, table_definition):
        """ Create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(table_definition)
        except sqlite3.Error as e:
            print(e)
            raise RuntimeError('db.py: create_table()') from e


    # Generic SQL operations
    def insert_or_update_or_delete(self, sql_cmd, obj):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql_cmd, obj)
            self.db.commit()
        except sqlite3.Error as e:
            print(e)
            raise RuntimeError('db.py: insert_or_update_or_delete()') from e


    def select(self, sql_cmd, obj=None):
        try:
            cursor = self.db.cursor()
            if obj:
                cursor.execute(sql_cmd, obj)
            else:
                cursor.execute(sql_cmd)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
            raise RuntimeError('db.py: select()') from e
            #return []


    # Player operations
    def create_player(self, account_id, username, replay_files):
        # If player already in db, update it
        if self.update_player(account_id, username, replay_files):
            return True

        player = (account_id, username, ','.join(replay_files), len(replay_files))
        insert_cmd = """
                        INSERT INTO players(account_id,username,replay_files,counter)
                        VALUES(?,?,?,?)
                     """
        self.insert_or_update_or_delete(insert_cmd, player)
        return True


    def update_player(self, account_id, username, replay_files):
        current_player = self.find_player(account_id)
        if current_player is None:
            return False

        if current_player[3] > 0 and len(replay_files) > 0:
            updated_replay_files = current_player[2] + ',' + ','.join(replay_files)
        else:
            updated_replay_files = current_player[2] + ','.join(replay_files)

        updated_player = (username,
                          updated_replay_files,
                          current_player[3] + len(replay_files),
                          account_id)

        update_cmd = """
                        UPDATE players
                        SET username = ? ,
                            replay_files = ? ,
                            counter = ?
                        WHERE account_id = ?
                     """
        self.insert_or_update_or_delete(update_cmd, updated_player)
        return True


    def delete_player(self, account_id):
        current_player = self.find_player(account_id)
        if current_player is None:
            return False

        delete_cmd = """
                        DELETE FROM players WHERE account_id = ?
                     """
        self.insert_or_update_or_delete(delete_cmd, (account_id,))
        return True


    def reset_player(self, account_id):
        current_player = self.find_player(account_id)
        if current_player is None:
            return False

        updated_player = (current_player[1], '', 0, current_player[0])
        update_cmd = """
                        UPDATE players
                        SET username = ? ,
                            replay_files = ? ,
                            counter = ?
                        WHERE account_id = ?
                     """

        self.insert_or_update_or_delete(update_cmd, updated_player)
        return True


    def find_player(self, account_id):
        select_cmd = 'SELECT * FROM players WHERE account_id=?'
        players_found = self.select(select_cmd, (account_id,))
    
        assert(len(players_found) <= 1)
        if len(players_found) == 0:
            return None

        return players_found[0]


    def find_all_players(self):
        select_cmd = 'SELECT * FROM players'
        players_found = self.select(select_cmd)

        return players_found


    def find_all_players_ids(self):
        players_found = self.find_all_players()
        return [p[0] for p in players_found]


    # Replay operations
    def create_replay(self, replay_file, time, players_ids):
        replay = (replay_file, time, ','.join(players_ids))

        # If replay already in db, don't add it
        if self.find_replay(replay_file):
            print('Already analyzed replay', replay_file)
            return False
    
        insert_cmd = """
                        INSERT INTO replays(replay_file,time,players_ids)
                        VALUES(?,?,?)
                     """
        self.insert_or_update_or_delete(insert_cmd, replay)
        return True


    def find_replay(self, replay_file):
        select_cmd = 'SELECT * FROM replays WHERE replay_file=?'
        replay_found = self.select(select_cmd, (replay_file,))
    
        assert(len(replay_found) <= 1)
        if len(replay_found) == 0:
            return None

        replay_found[2] = replay_found[2].split(',')
        return replay_found


    def find_all_replays(self):
        #select_cmd = 'SELECT * FROM replays'
        select_cmd = 'SELECT * FROM replays ORDER BY time ASC'
        replays_found = self.select(select_cmd)
    
        replays_found = list(map(lambda x: [x[0], x[1], x[2].split(',')], replays_found))
        return replays_found


    def find_last_replay(self):
        replays_found = self.find_all_replays()
        if len(replays_found):
            return replays_found[-1][0], replays_found[-1][1]

        return None, None


    def close(self):
        if self.db is not None:
            self.db.close()
