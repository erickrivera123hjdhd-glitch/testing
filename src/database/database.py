import sqlite3
import json
import os
from datetime import datetime

class Database:
    def __init__(self, db_path='data/bot.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS connections
                     (id INTEGER PRIMARY KEY, user_id TEXT, session_token TEXT,
                      connected BOOLEAN, last_command TEXT, last_response TEXT,
                      connected_at TIMESTAMP, last_activity TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id TEXT PRIMARY KEY, allowed BOOLEAN, added_at TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS roles
                     (role_id TEXT PRIMARY KEY, allowed BOOLEAN, added_at TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (id INTEGER PRIMARY KEY, timestamp TIMESTAMP, message TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS script_history
                     (id INTEGER PRIMARY KEY, user_id TEXT, script TEXT,
                      executed_at TIMESTAMP, result TEXT, success BOOLEAN)''')
        c.execute('''CREATE TABLE IF NOT EXISTS settings
                     (key TEXT PRIMARY KEY, value TEXT)''')
        conn.commit()
        conn.close()

    def add_connection(self, user_id, session_token):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO connections
                     (user_id, session_token, connected, last_command, last_response,
                      connected_at, last_activity)
                     VALUES (?, ?, 1, '', '', ?, ?)''',
                  (user_id, session_token, datetime.now(), datetime.now()))
        conn.commit()
        conn.close()

    def update_connection(self, user_id, last_command=None, last_response=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if last_command:
            c.execute('UPDATE connections SET last_command = ?, last_activity = ? WHERE user_id = ?',
                      (last_command, datetime.now(), user_id))
        if last_response:
            c.execute('UPDATE connections SET last_response = ?, last_activity = ? WHERE user_id = ?',
                      (last_response, datetime.now(), user_id))
        conn.commit()
        conn.close()

    def disconnect(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE connections SET connected = 0, last_activity = ? WHERE user_id = ?',
                  (datetime.now(), user_id))
        conn.commit()
        conn.close()

    def get_connection(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM connections WHERE user_id = ? AND connected = 1', (user_id,))
        result = c.fetchone()
        conn.close()
        return result

    def get_all_connections(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM connections WHERE connected = 1')
        results = c.fetchall()
        conn.close()
        return results

    def add_log(self, message):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO logs (timestamp, message) VALUES (?, ?)',
                  (datetime.now(), message))
        conn.commit()
        conn.close()

    def get_logs(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT timestamp, message FROM logs ORDER BY id DESC LIMIT ?', (limit,))
        results = c.fetchall()
        conn.close()
        return results

    def is_user_allowed(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT allowed FROM users WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result and result[0] == 1

    def is_role_allowed(self, role_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT allowed FROM roles WHERE role_id = ?', (role_id,))
        result = c.fetchone()
        conn.close()
        return result and result[0] == 1

    def add_user(self, user_id, allowed=True):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO users (user_id, allowed, added_at)
                     VALUES (?, ?, ?)''', (user_id, allowed, datetime.now()))
        conn.commit()
        conn.close()

    def remove_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

    def add_role(self, role_id, allowed=True):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO roles (role_id, allowed, added_at)
                     VALUES (?, ?, ?)''', (role_id, allowed, datetime.now()))
        conn.commit()
        conn.close()

    def remove_role(self, role_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM roles WHERE role_id = ?', (role_id,))
        conn.commit()
        conn.close()

    def save_script_history(self, user_id, script, result, success):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO script_history (user_id, script, executed_at, result, success)
                     VALUES (?, ?, ?, ?, ?)''', (user_id, script, datetime.now(), result, success))
        conn.commit()
        conn.close()

    def get_setting(self, key):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def set_setting(self, key, value):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)''', (key, value))
        conn.commit()
        conn.close()
