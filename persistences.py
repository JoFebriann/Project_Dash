from kink import di, inject
from sqlite3 import Error

from project_dash.dtos import EmailDTO, LoginDTO, RegisterDTO, UserDTO, LeaderboardDTO

import os
import sqlite3


@inject
class DashSqlDb:
    def __init__(self, db_init: str, db_filename: str, main_dir: str):
        self.db_init = db_init
        self.db_filename = db_filename
        self.db_path = os.path.join(main_dir, db_filename)

        # inisialisasi connection
        self.conn = None
        self.cursor = None


        self.setup_database()

    def setup_database(self):
        if self.db_init == "True":
        # if self.db_init == "True" or os.getenv("PYCHARM_HOSTED") is not None:
            self.recreate_database()

        self.conn = self.create_connection(self.db_path)
        self.cursor = self.conn.cursor()

        if self.db_init == "True":
        # if self.db_init == "True" or os.getenv("PYCHARM_HOSTED") is not None:
            self.setup_db()

    def recreate_database(self):
        if os.path.exists(self.db_path):  # hapus file .db yang sudah ada
            self.delete_database()

        with open(self.db_filename, "w") as db_file:  # kemudian buat file .db baru
            pass

    def delete_database(self):
        self.cursor.close() if self.cursor is not None else None
        self.conn.close() if self.conn is not None else None
        os.remove(self.db_path)

    def create_connection(self, db_path):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)
        
        return conn
    
    def setup_db(self):
        sql_setup_table = """CREATE TABLE player_data (
                            username TEXT,
                            email TEXT,
                            score INT,
                            PRIMARY KEY (username)
        )"""

        self.cursor.execute(sql_setup_table)
        self.conn.commit()
    
    def register_acc(self, _register_dto: RegisterDTO) -> None:
        temp_username = _register_dto.username
        temp_email = _register_dto.email

        sql_insert_player = f'''
                INSERT INTO player_data VALUES (?, ?, 0)''' 
        
        self.cursor.execute(sql_insert_player, (temp_username, temp_email, ))
        self.conn.commit()

    def insert_acc(self, _username: str, _email: str, _score: int) -> None:
        sql_insert_player = f'''
                INSERT INTO player_data VALUES (?, ?, ?)'''

        self.cursor.execute(sql_insert_player, (_username, _email, _score, ))
        self.conn.commit()
        
    def show_players(self):
        sql_show_players = '''SELECT * FROM player_data'''

        all_records = self.cursor.execute(sql_show_players)
        self.conn.commit()

        results = []
        for row in all_records:
            results.append(UserDTO(row[0], row[1], row[2]))
        
        return results
    
    def set_high_scores(self, _username, _score):
        sql_high_score = '''UPDATE player_data
                            SET score = ?
                            WHERE username = ? AND score < ?'''
        
        all_records = self.cursor.execute(sql_high_score, (_score, _username, _score))
        
        results = []
        for row in all_records:
            results.append(UserDTO(row[0], row[1], row[2]))
        
        return results
    
    def get_leaderboards(self):
        sql_top_five = '''SELECT username, score FROM player_data
        ORDER BY score DESC
        LIMIT 5
        '''

        all_records = self.cursor.execute(sql_top_five)
        self.conn.commit()

        results = []
        for row in all_records:
            results.append(LeaderboardDTO(row[0], row[1]))
        
        return results
    
    def get_top_player(self):
        sql_top_player = f'''SELECT username, email, score
                            FROM player_data
                            WHERE score = (SELECT MAX(score) FROM player_data);'''
        
        record = self.cursor.execute(sql_top_player).fetchone()
        result = UserDTO(record[0], record[1], record[2])
        
        return result
    
    def get_exact_player(self, _username: str): 
        sql_exact_player = f'''SELECT username, email, score
                            FROM player_data
                            WHERE username = ?;'''
        
        record = self.cursor.execute(sql_exact_player, (_username, )).fetchone()
        result = UserDTO(record[0], record[1], record[2])
        
        return result
    
    def get_email(self, _username: str):
        sql_get_email = f'''SELECT email FROM player_data
        WHERE username = ?
        '''

        all_records = self.cursor.execute(sql_get_email, (_username, ))

        results = []
        for row in all_records.fetchall():
            results.append(EmailDTO(row[0]))  # row[0] ?

        return results[0].email
    
    def search_player(self, _username):
        sql_search = f'''SELECT * FROM player_data WHERE username = ?'''
        all_records = self.cursor.execute(sql_search, (_username, ))
        
        results = []
        for row in all_records:
            results.append(UserDTO(row[0], row[1], row[2]))
            
        return results
    
    def add_score(self, _username, _score):
        sql_search = f'''UPDATE player_data 
                        SET score = ?
                        WHERE username = ? AND score < ?'''
        all_records = self.cursor.execute(sql_search, (_score, _username, _score, ))
        
        results = []
        for row in all_records:
            results.append(UserDTO(row[0], row[1], row[2]))
            
        return results