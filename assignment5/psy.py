#!/usr/bin/python3
import psycopg2
import json
import sys
from types import *

def runPsy(conn, curs, jsonFile):
    with open(jsonFile) as f:
        for line in f:
            data = json.loads(line) 

            # check newcustomer exist 
            if 'newcustomer' in data: 
                
                cusData = data['newcustomer']

                # check whether customerid exist 
                curs.execute("""
                select count(*) from customers where customerid = %s
                """, (cusData['customerid'], ))
                existed = curs.fetchone()

                # if not exist 
                if existed == (0,): 
                    
                    # count # of frequentflieron does not have a match in the airlines table
                    curs.execute("""
                    select count(*) from airlines where name = %s
                    """, (cusData['frequentflieron'], ))
                    noairlines = curs.fetchone()

                    # if the frequentflieron does not have a match in the airlines table
                    if noairlines == (0,):
                            print("Error424")
                            exit()

                    # if the frequentflieron have a match in the airlines table
                    else: 
                        # change name to id 
                        curs.execute("""
                        select airlineid from airlines where name = %s
                        """, (cusData['frequentflieron'], ))
                        idnum = curs.fetchone()

                        # insert value 
                        curs.execute("""
                        INSERT INTO customers (customerid, name, birthdate, frequentflieron )
                        VALUES (%s, %s, %s, %s);
                        """,
                        (cusData['customerid'], cusData['name'], cusData['birthdate'],idnum))
                
                # if exist then exit and print Error424 
                else: 
                    print("Error424")
                    exit()

                    # check flightinfo exist
            elif 'flightinfo' in data: 
 
                fliData = data['flightinfo']
 
                 # check whether customerid exist 
                for customer in fliData['customers']: 
                    cusdata = customer 
                    
                    curs.execute("""
                    select count(*) from customers where customerid = %s
                    """, (cusdata['customerid'], ))
                    countnum = curs.fetchone()
 
                # if not exist 
                    if countnum == (0,): 
                        curs.execute("""
                        select count(*) from airlines where airlineid = %s
                        """, (cusdata['frequentflieron'], ))
                        noairlines = curs.fetchone()

                        if noairlines == 0:
                            print("Error424")
                            exit()
 
                        # if the frequentflieron have a match in the airlines table
                        else: 
                            # change name to id 
                            curs.execute("""
                            select airlineid from airlines where airlineid = %s
                            """, (cusdata['frequentflieron'], ))
                            idnum = curs.fetchone()
 
                            # insert value 
                            curs.execute("""
                            INSERT INTO customers (customerid, name, birthdate, frequentflieron )
                            VALUES (%s, %s, %s, %s);
                            """,
                            (cusdata['customerid'], cusdata['name'], cusdata['birthdate'], cusdata['frequentflieron']))
                

                    curs.execute("""
                    INSERT INTO flewon (flightid, customerid, flightdate)
                    VALUES (%s, %s, %s);
                    """,
                    (fliData['flightid'], cusdata['customerid'], fliData['flightdate']))

          



        conn.commit()
