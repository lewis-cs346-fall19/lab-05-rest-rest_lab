#! /usr/bin/python3

import json
import MySQLdb
import passwords
import cgi
import os
#========status check=======
print("Content-Type: text/json")
print("Status: 200 OK")
print()
#========content============

conn = MySQLdb.connect(host   = passwords.SQL_HOST,
                        user   = passwords.SQL_USER,
                        passwd = passwords.SQL_PASSWD,
                        db     = "db0")
cur = conn.cursor()
cur.execute("SELECT * FROM table1")
return_val = cur.fetchall()
cur.close()
user = []
for i in return_val:
    user.append({"ID":i[0],"username":i[1],"userage":i[2],"URL":"http://ec2-34-226-154-175.compute-1.amazonaws.com/cgi-bin/path.cgi/user/"+str(i[0])})
user_json = json.dumps(user,indent=2)
if "PATH_INFO" in os.environ:
    path = os.environ["PATH_INFO"]
else:
    path = "/"
path = path.split("/")
print(path)
if path[1] == "user" and len(path) == 3 and path[2].isdigit()==False:
    print(user_json)

if path[1] == "user" and path[2].isdigit()==True:
    print(json.dumps(user[int(path[2])-1],indent = 2))

form = cgi.FieldStorage()

if form != {} and path[1] == "user" and len(path) == 3 and path[2].isdigit()==False:
    cur = conn.cursor()
    cur.execute("INSERT INTO table1(fname,age) VALUES(%s,%s);",(form["username"].value,form["userage"].value))
    new_id = cursor.lastrowid
    cur.close()
    print("Status: 302 Redirect")
    loc = "http://ec2-34-226-154-175.compute-1.amazonaws.com/cgi-bin/path.cgi/user/"+new_id+"/"
    print("Location: "+loc)
