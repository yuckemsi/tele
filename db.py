import sqlite3

_connection = None


def get_connection():
    global _connection
    if _connection is None:
        _connection = sqlite3.connect('wish.db', check_same_thread=False)
    return _connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
		CREATE TABLE IF NOT EXISTS user_message(
			id			INTEGER PRIMARY KEY,
			user_id		INTEGER NOT NULL,
			username	STRING NOT NULL,
			text		TEXT NOT NULL
		)
	''')

    conn.commit()


def add_message(user_id: int, username: str, text: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, username, text) VALUES (?, ?, ?)', (user_id, username, text))
    conn.commit()

def count_messages(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_message WHERE user_id = ? LIMIT 1', (user_id,))
    (res,) = c.fetchone()
    return res

def list_messages(user_id: int, limit: int = 10):
    conn = get_connection()
    c = conn.cursor()

    c.execute('SELECT text FROM user_message WHERE user_id = ?  ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()


if __name__ == '__main__':
    init_db()
    

    r = count_messages(user_id=123)
    print(r)

    r = list_messages(user_id=123, limit=2)
    for i in r:
        print(r)
