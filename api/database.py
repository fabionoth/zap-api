import sqlite3


DATABASE_FILE = 'running.db'

class Database:

    def __init__(self, conn, debug = False):
        self.__conn = conn
        self.__debug = debug
        self.__generate_initial_table()

    def __init__(self, debug = False):
        self.__debug = debug
        self.__conn = sqlite3.connect(DATABASE_FILE)
        self.__generate_initial_table()

    def __exit__(self):
        self.__conn.close()
        self.close()

    @property
    def connection(self):
        return self.__conn

    def update_status(self, name, status = "Starting Analysys..."):
        c = self.__conn.cursor()
        #verify if has status in this app
        if c.execute("SELECT id FROM running WHERE app LIKE ? LIMIT 1",name).fetchall():
            c.execute("INSERT INTO running (app, status) VALUES(?,?)", name, status)
            c.commit()
        else :
            c.execute("UPDATE running SET status = ? WHERE app like ?", (status, name))
            c.commit()

        if self.__debug:
            print("DEBUG: UPDATED STATUS \n APP:{} \n STATUS:{}".format(app, status))

    def __generate_initial_table(self):
        c = self.__conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS running (id integer primary key autoincrement, app text, status text)''')
        __conn.commit()

        if self.__debug:
            print("DEBUG: Create table. If not exists")

    
    