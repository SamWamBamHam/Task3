import sqlite3

def getAll(username):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM users WHERE username == '{username}';")
    return result.fetchone()

def login(username, password):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute(f"SELECT password FROM users WHERE username == '{username}';")
    result = result.fetchone()
    if type(result) == tuple:
        if result[0] == password:
            return True
        else:
            return False
    else:
        return False