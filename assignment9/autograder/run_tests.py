import json
import math
import os
import random
import re
import subprocess
import sys
import traceback
from functools import wraps
import errno
import signal
import pickle

from disk_relations import *
from transactions import *
import time
from exampletransactions import *

import copy

test_name = sys.argv[1]
max_score = -1

results_file_name = '/autograder/results/results.json'
#results_file_name = 'results.json'

def add_test_result_and_update_file(score, output):
    try:
        with open(results_file_name, 'r') as f:
            results_json = json.load(f)
            results_json['tests'].append({"score": score, "max_score": max_score, "name": "", "number": test_name, "output": output}) 
        with open(results_file_name, 'w') as f:
            json.dump(results_json, f)
    except:
        pass
    os._exit(0)

def runTransactions(tname, tlist):
    for l in tlist:
        threading.Thread(target=tname, args=l).start()
        time.sleep(2)

def runTransactionsNoDelay(tname, tlist):
    for l in tlist:
        threading.Thread(target=tname, args=l).start()

def killAfterSomeTime():
    print("----- STARTING TIMER")
    for i in range(0, 50):
        time.sleep(4)
        print("----- CONTINUING TIMER" + str(i))
    print("----- FAILED with TIME OUT")
    add_test_result_and_update_file(0, "--- FAILED with TIME OUT")


################################################################################################################################################
################################################################################################################################################
def run_test_ixlock():
    bpool = BufferPool()
    r = Relation(sys.argv[2])
#LogManager.setAndAnalyzeLogFile(sys.argv[3])

    runTransactions(Transaction1, [(r, "0", 20), (r, "10", 20)])
    time.sleep(3)
    runTransactions(TransactionReadRelation, [(r, 20)])
    time.sleep(10)

    for (k, v) in LockTable.lockhashtable.items():
        print("Object {}; current: {}; waiting: {}".format(k, v.current_transactions_and_locks, v.waiting_transactions_and_locks))

    correct = dict()
    #correct["0"] = "Object 0; current: [(1, 1)]; waiting: []"
    correct["relation1"] = "Object relation1; current: [(1, 1)]; waiting: [(3, 0), (2, 1)]"
    #correct["10"] = "Object 10; current: [(2, 1)]; waiting: []"
    for (k, v) in LockTable.lockhashtable.items():
        s = "Object " + str(k) + "; current: " + str(v.current_transactions_and_locks) + "; waiting: " + str(v.waiting_transactions_and_locks)
        if s != correct[k]:
            print("-- FAILED --")
            add_test_result_and_update_file(0, "--- FAILED")

    print("-- PASSED --")
    add_test_result_and_update_file(max_score, "--- PASSED")


################################################################################################################################################
################################################################################################################################################
def run_deadlock_test():
    with open('{}.pickle'.format(sys.argv[1]), "rb") as f:
        LockTable.lockhashtable = pickle.load(f)
    LockTable.compatibility_list = [(LockTable.IS, LockTable.IS), (LockTable.IS, LockTable.S), (LockTable.S, LockTable.IS), (LockTable.S, LockTable.S), (LockTable.IX, LockTable.IX), (LockTable.IX, LockTable.IS), (LockTable.IS, LockTable.IX)]
    if sys.argv[1] == 'test-deadlocks-1':
        possible = [set([1]), set([2]), set([3])]
    elif sys.argv[1] == 'test-deadlocks-2':
        possible = [set([1, 3]), set([1, 4]), set([2, 3]), set([2, 4])]
    elif sys.argv[1] == 'test-deadlocks-3':
        possible = [set([1]), set([3]), set([4])]
    elif sys.argv[1] == 'test-deadlocks-4':
        possible = [set([])]
    elif sys.argv[1] == 'test-deadlocks-5':
        possible = [set([1, 2, 3, 4]), set([5])]
    elif sys.argv[1] == 'test-deadlocks-6':
        possible = [set([1, 2, 3, 4]), set([5]), set([6])]
    elif sys.argv[1] == 'test-deadlocks-7':
        possible = [set([])]
    elif sys.argv[1] == 'test-deadlocks-8':
        possible = [set([1, 2, 3]), set([2, 3, 4]), set([2, 3, 7]), set([3, 4, 5]), set([3, 4, 7]), set([1, 2, 6]), set([4, 5, 6]), set([6, 7])]
    try:
        print("Calling deadlock detection code...")
        for (k, v) in LockTable.lockhashtable.items():
            print("Object {}; current: {}; waiting: {}".format(k, v.current_transactions_and_locks, v.waiting_transactions_and_locks))
        ret = sorted(LockTable.detectDeadlocksAndChooseTransactionsToAbort())
        print("Need to abort transactions: " + str(ret))
        print("Answer should be one of: " + str(possible))

        if any(ret == list(x) for x in possible):
            print("----- PASSED")
            add_test_result_and_update_file(max_score, "--- PASSED")
        else:
            print("----- FAILED")
            add_test_result_and_update_file(0, "--- FAILED")
    except:
        e = sys.exc_info()
        print("-----------------> Failed with exception" + str(e[0]))
        print(traceback.format_exc())
        print("----- FAILED")
        add_test_result_and_update_file(0, "Failed -- Exception {}".format(traceback.format_exc()))


################################################################################################################################################
################################################################################################################################################
def run_test_recovery(testno):
    try:
        bpool = BufferPool()
        relationname = "recoverytest{}_relation".format(testno)
        logfile = "recoverytest{}_logfile".format(testno)
        r = Relation(relationname)
        print("Starting to analyze the logfile {}".format(logfile))
#LogManager.setAndAnalyzeLogFile(logfile)

        correctrelationname = "recoverytests-answers/recoverytest{}_relation".format(testno)
        correctlogfile = "recoverytests-answers/recoverytest{}_logfile".format(testno)
        print("Comparing the relations")
        rel1 = open(relationname, 'r').read()
        rel2 = open(correctrelationname, 'r').read()
        if len(rel1) != len(rel2):
            print("The two files are not the same length")
        diff1 = ""
        diff2 = ""
        for i in range(Globals.blockSize, min(len(rel1), len(rel2))): 
            if rel1[i] != rel2[i]:
                print("difference at character {}: rel1 = {} and rel2 = {}".format(i, rel1[i], rel2[i]))
                diff1 += rel1[i]
                diff2 += rel2[i]
            #else:
                #print "same character {}: rel1 = {} and rel2 = {}".format(i, rel1[i], rel2[i])
        print("Comparing the logfiles")
        subprocess.call(["diff", logfile, correctlogfile])
        if diff1 == "":
            print("-- PASSED --")
            add_test_result_and_update_file(max_score, "--- PASSED")
            os._exit(0)
        else:
            print("-- FAILED --")
            print("-- diff1: {}".format(diff1))
            print("-- diff2: {}".format(diff2))
            add_test_result_and_update_file(0, "--- FAILED")
    except:
        e = sys.exc_info()
        print("-----------------> Failed with exception" + str(e[0]))
        print(traceback.format_exc())
        print("----- FAILED")
        add_test_result_and_update_file(0, "Failed -- Exception {}".format(traceback.format_exc()))
        
################################################################################################################################################
################################################################################################################################################

def wound_wait_test():
        waiting_transactions_and_locks_list = [(1,1),(2,1),(3,1),(5,1),(6,1)]
        abortList = LockTable.woundWait(waiting_transactions_and_locks_list, 4)
        correct = [5,6]
        print("AbortList",abortList)
        if abortList != correct:
            print("-- FAILED --")
            add_test_result_and_update_file(0, "--- FAILED")

        else:
            print("-- PASSED --")
            add_test_result_and_update_file(max_score, "--- PASSED")

            
            


################################################################################################################################################
################################################################################################################################################
##################################### We will run these one by one
################################################################################################################################################
################################################################################################################################################

if sys.argv[1] in ['test-ixlock']:
    if len(sys.argv) != 4:
        print("Need to specify the relation name, logfile to use and which test to run")
        os._exit(1)
    max_score = 0.5
    run_test_ixlock()
elif sys.argv[1] == 'test-recovery':
    if len(sys.argv) != 3:
        print("Need to specify the test number")
        os._exit(1)
    test_no = sys.argv[2]
    max_score = .1875
    test_name = "{}-{}".format(test_name, sys.argv[2])
    run_test_recovery(test_no)
elif sys.argv[1] in ['test-deadlocks-{}'.format(i) for i in [1, 2, 3, 4, 5, 6, 7, 8]]:
    if len(sys.argv) != 4:
        print("Need to specify the relation name, logfile to use and which test to run")
        os._exit(1)
    max_score = .1875
    bpool = BufferPool()
    r = Relation(sys.argv[2])
#LogManager.setAndAnalyzeLogFile(sys.argv[3])
    run_deadlock_test()
elif sys.argv[1] in ['test-woundwait']:
    max_score = 0.5
    wound_wait_test()
    
