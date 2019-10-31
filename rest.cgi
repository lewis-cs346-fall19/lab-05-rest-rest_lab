#! /usr/bin/python3

import json
import MySQLdb
import passwords
import cgi
import os

#========status============
#print("Content-Type: text/json")
#print("Status: 200 OK")
#print()
#========content============

conn = MySQLdb.connect(host   = passwords.SQL_HOST,
                        user   = passwords.SQL_USER,
                        passwd = passwords.SQL_PASSWD,
                        db     = "db0")
def get_db(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM table1")
    return_val = cur.fetchall()
    cur.close()
    return return_val

def edit(conn,fname,age):
    cur = conn.cursor()
    cur.execute("INSERT INTO table1 (User,Age) VALUES(%s,%s);",(fname,age,))
    new_id = cur.lastrowid
    cur.close()
    return new_id

return_val = get_db(conn)

def get_json(return_val):
    user = []
    for i in return_val:
        user.append({"ID":i[0],"User":i[1],"Age":i[2],"URL":"http://ec2-34-226-154-175.compute-1.amazonaws.com/cgi-bin/rest.cgi/user/"+str(i[0])})
    user_json = json.dumps(user,indent=2)
    return user

if "PATH_INFO" in os.environ:
    path = os.environ["PATH_INFO"]
else:
    path = "/"
path = path.split("/")

if path[1] == "user" and len(path) == 3 and path[2].isdigit()==False and path[2]!="form":
    return_val = get_db(conn)
    user = get_json(return_val)
    user_json = json.dumps(user,indent=2)
    print("Content-Type: text/json")
    print("Status: 200 OK")
    print()
    print(user_json)

if path[1] == "user" and path[2].isdigit()==True:
    return_val = get_db(conn)
    user = get_json(return_val)
    user = user[int(path[2])-1]
    user_json = json.dumps(user,indent=2)
    print("Content-Type: text/json")
    print("Status: 200 OK")
    print()
    print(user_json)

if path[1] == "user" and path[2] == "form":
    print("Status: 302 Redirect")
    form = cgi.FieldStorage()
    fname = form["user"].value
    age = form["age"].value
    id = edit(conn,fname,age)
    conn.commit()
    conn.close()
    loc = "Location: http://ec2-34-226-154-175.compute-1.amazonaws.com/cgi-bin/rest.cgi/user/"+str(id)
    print(loc)
    print()
