from disk_relations import *
from transactions import *
import time
from exampletransactions import *

#####################################################################################################
####
#### Some testing code
####
#####################################################################################################
# Initial Setup
bpool = BufferPool()
r = Relation('relation1')

# Start the transactions

def testingSnapshot():

    print("\n\n\n\n")
    testingSnapshotAB1()

    print("\n\n\n\n")
    testingSnapshotAB2()

    print("\n\n\n\n")
    testingSnapshotAggregate()

    print("\n\n\n\n")
    testingSnapshotSlowAbort()

    print("\n\n\n\n")
    testingMultiWrite()
    
# overlapping transactions, not overlapping writesets: both write one var, then read the next, both see the initial value (impossible w/ serializability)
def testingSnapshotAB1():

    # init 0,1 to zeros, so that we can distinguish from the default "10"'s
    setVal("0", "0")
    setVal("1", "0")

    t = threading.Thread(target=TransactionSnapshotXY, args=(r, "0", "1", "2", 1))
    t.start()

    time.sleep(0.2)

    t = threading.Thread(target=TransactionSnapshotXY, args=(r, "1", "0", "3", 1))
    t.start()

    waitChildren()

    res = (getVal("0")=="1") and (getVal("0")=="1") and (getVal("2")=="0") and (getVal("3")=="0")
    print("testingSnapshotAB1 returns {}".format(res))
    

# non-overlapping transactions: second should see the other's write
def testingSnapshotAB2():
    setVal("4", "0")
    setVal("5", "0")

    t = threading.Thread(target=TransactionSnapshotXY, args=(r, "5", "4", "6", 0))
    t.start()

    time.sleep(1)
    
    t = threading.Thread(target=TransactionSnapshotXY, args=(r, "4", "5", "7", 0))
    t.start()

    waitChildren()

    res = (getVal("4")=="1") and (getVal("5")=="1") and (getVal("6")=="0") and (getVal("7")=="1")
    print("testingSnapshotAB2 returns {}".format(res))
    
# also overlapping trans, not overlapping writesets: neither should see the other's write, leading both to change "their" variable to make the sum be 100
def testingSnapshotAggregate():
    t = threading.Thread(target=TransactionSnapshotAggregate, args=(r, "8", "9"))
    t.start()

    t = threading.Thread(target=TransactionSnapshotAggregate, args=(r, "9", "8"))
    t.start()

    waitChildren()

    res = (getVal("8")=="90") and (getVal("9")=="90")
    print("testingSnapshotAggregate returns {}".format(res))


## two writes to same var, first one is slower to commit and should abort
def testingSnapshotSlowAbort():
    t = threading.Thread(target=TransactionSlowWriter, args=(r, "10", "11", 2))
    t.start()

    t = threading.Thread(target=TransactionSlowWriter, args=(r, "10", "12", 1))
    t.start()
    waitChildren()

    res = (getVal("10")=="12")
    print("testingSnapshotSlowAbort returns {}".format(res))


## two writes to same var, first one is slower to commit and should abort
def testingMultiWrite():
    t = threading.Thread(target=TransactionMultiWrite, args=(r, "11", "13", "5", 1))
    t.start()

    time.sleep(0.5)
    
    t = threading.Thread(target=TransactionMultiWrite, args=(r, "12", "14", "5", 1))
    t.start()
    waitChildren()

    res = (getVal("11")=="5") and (getVal("12")=="5") and (getVal("13")=="5") and (getVal("14")=="5")
    print("testingSnapshotMultiWrite returns {}".format(res))


def getVal(id):
    return r.getTuple(id).getAttribute("A")

def setVal(id, val):
    r.getTuple(id).setAttribute("A", val)

def waitChildren():
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    
testingSnapshot()

### Start a thread to periodically check for deadlocks
#t = threading.Thread(target=LockTable.detectDeadlocks())
#t.start()

### Wait for all the threads to complete
waitChildren()
BufferPool.writeAllToDisk(r)
