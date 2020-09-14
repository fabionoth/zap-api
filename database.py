import sqlite3

class Database:

    DATABASE_FILE = 'running.db'

    def __init__(self, conn, debug = False):
        self.__conn = conn
        self.__debug = debug
        self.__generate_initial_table()

    def __init__(self, debug = False):
        self.__debug = debug
        self.__conn = sqlite3.connect(self.DATABASE_FILE)
        self.__generate_initial_table()

    def __exit__(self):
        self.__conn.close()

    @property
    def connection(self):
        return self.__conn

    def update_status(self, name, status = "Starting Analysys..."):
        c = self.__conn.cursor()
        #verify if has status in this app
        c.execute("SELECT id FROM running WHERE app like '{}' LIMIT 1".format(name))
        data = c.fetchall()
        if not data:
            c.execute("INSERT INTO running (app, status) VALUES(?,?)", (name, status))
        else :
            c.execute("UPDATE running SET status = ? WHERE app like ?", (status, name))
        
        self.__conn.commit()
        if self.__debug:
            print("DEBUG: UPDATED STATUS \n APP:{} \n STATUS:{}".format(name, status))
            
    def get_reports(self):
        c = self.__conn.cursor()
        c.execute("SELECT app, status FROM running ORDER BY id DESC")
        return c.fetchall()

    def __generate_initial_table(self):
        c = self.__conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS running (id integer primary key autoincrement, app text, status text)''')
        self.__conn.commit()

        if self.__debug:
            print("DEBUG: Create table. If not exists")

    
    