# Process finance data into database
import psycopg

class DatabaseOps:

    def __init__(self,
                 dbname: str="database",
                 user: str="postgres",
                 host: str="127.0.0.1",
                 port: str="8080") -> None:
        self.__dbname = dbname
        self.__user = user
        self.__host = host
        self.__port = port

    # returns cursor
    def __connect(self):
        self.__conn = psycopg.connect(database=self.__dbname,
                                      user=self.__user,
                                      host=self.__host,
                                      port=self.__port)
        self.__cur = self.__conn.cursor()

    def __disconnect(self):
        if self.__cur != None:
            self.__cur.close()
            self.__conn.close()

    def execute(self, command: str):
        self.__cur.execute(command)
        self.__conn.commit()