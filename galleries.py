import MySQLdb
from config import Config

db = MySQLdb.connect(**Config.getAllParams())

cursor = db.cursor()

cursor.execute("select * from people")
print len(cursor.fetchall())

#select * from people where peopleid in (select person from probe) and cameraid="C1" and bb_x<800 and bb_y>150;