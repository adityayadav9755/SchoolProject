import mysql.connector as sqlt
con = sqlt.connect(host="localhost",user="root",password='Aditya2612',database='project1')
cur=con.cursor()

cur.execute("alter table supplier modify mobile bigint(13);")
con.commit()

