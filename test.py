#!/usr/bin/python
import MySQLdb as mdb
import sys
try:
    f = open("../mysqlinfo")
    usrnm = f.readline()[:-1]
    psswd = f.readline()[:-1]
    con = mdb.connect('localhost',usrnm,psswd,'registrar')
    cur = con.cursor()
    cur.execute("SELECT * FROM Course")
    ver = cur.fetchall()
    
    print ver
except:
    print "ERROR"
    sys.exit(1)
finally:
    if not con == None:
        con.close()
