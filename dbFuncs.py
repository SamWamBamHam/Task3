import sqlite3

def getAll(username: str):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM users WHERE username == '{username}';")
    return result.fetchone()

def addToVars(username: str, newWins: int = 0, newGames: int = 0, newTime: int = 0, newFlags: int = 0, newRevealed: int = 0):
    null1, null2, games, wins, time, flags, revealed = getAll(username)
    del null1, null2
    wins += newWins
    games += newGames
    time += newTime
    flags += newFlags
    revealed += newRevealed
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(f"UPDATE users SET totalGames = {games}, totalWins = {wins}, totalTime = {time}, totalFlags = {flags}, totalRevealed = {revealed} WHERE username = '{username}';")
    con.commit()

def login(username: str, password: str):
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
    
def signUp(username: str, password: str):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM users WHERE username == '{username}';")
    if type(result.fetchone()) == tuple:
        return False
    else:
        cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}');")
        con.commit()
        return True