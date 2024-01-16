import sys
import time
import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', password='1234',db='health',charset='utf8')
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
try :
	with conn.cursor() as cur :
		sql = "select * from push_up"
		cur.execute(sql)
		cur.execute("INSERT INTO push_up(datetime,state) VALUES(current_time,'abc')")
		conn.commit()
		cur.execute(sql)
		for row in cur.fetchall() :
			print(row[0],row[1])
finally :
	conn.close()
	
