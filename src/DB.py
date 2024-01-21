import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', password='1234',db='health',charset='utf8')
        self.cursor = self.db.cursor()
    def show(self):
        sql = "SELECT * from push_up"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return(result)

if __name__ == "__main__":
  db = Database()
  db.show()
