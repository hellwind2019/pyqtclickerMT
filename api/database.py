import sqlite3



DB_NAME = "clicker.db"
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            score INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS upgrades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            level INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()
def __enter__(self):
   self.init_table()
   self.conn = sqlite3.connect(self.dbname)
   self.conn.row_factory = sqlite3.Row
   self.cursor = self.conn.cursor()
   return self

def __exit__(self, exc_type, exc_value, traceback):
   if self.conn:
       self.conn.commit()
       self.conn.close()

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, score FROM users').fetchall()
    conn.close()
    return [dict(user) for user in users]

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        user_id = None
    conn.close()
    return user_id

def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute(
        'SELECT id, username FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    conn.close()
    return dict(user) if user else None