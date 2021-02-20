import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse
import pickle

from psy import *
from orm import *

correct_answers = []

def pout(ans):
    print("--------- Your Query Answer ---------")
    for t in ans:
        print(t)
    print("")

def executePrint(s):
        cur.execute(s)
        ans = cur.fetchall()
        print(ans)
        return ans

correct_answers = []

conn = psycopg2.connect("dbname=flightsskewed user=vagrant")
cur = conn.cursor()

try:
    cur.execute("DELETE FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
    cur.execute("DELETE FROM customers WHERE (customerid='cust1000')")
    cur.execute("DELETE FROM customers WHERE (customerid='cust1001')")
    conn.commit()
    
    print("========== Executing PSY")
    runPsy(conn, cur, "example.json")

    cur.execute("SELECT * FROM customers WHERE customerid='cust1000'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    cur.execute("SELECT * FROM customers WHERE customerid = 'cust1001'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    cur.execute("SELECT flightid, customerid, flightdate FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    conn.commit()

    cur.execute("DELETE FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
    cur.execute("DELETE FROM customers WHERE (customerid='cust1000')")
    cur.execute("DELETE FROM customers WHERE (customerid='cust1001')")
    conn.commit()
    
    print("========== Executing ORM")

    runORM("example.json")

    cur.execute("SELECT * FROM customers WHERE customerid='cust1000'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    cur.execute("SELECT * FROM customers WHERE customerid = 'cust1001'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    cur.execute("SELECT flightid, customerid, flightdate FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    conn.commit()
	
except:
    print(sys.exc_info())
    raise

            

with open("correct_answers.pickle", "wb") as f:
    pickle.dump(correct_answers, f)

print("wrote {} answers".format(len(correct_answers)))
