## Project 5: Transactions, CMSC424, Fall 2019
**v1.03**

**(Due Dec 8, midnight)**

*The assignment is to be done by yourself.*

### Overview

In this project, you will modify a very simple database system that we have written to illustrate some of the transactions functionality.
The database system is written in Python and attempts to simulate how a database system would work, including what blocks it would read from disk, etc.

**NOTE**: This codebase is different from the Project 4 codebase, with simpler relation schema and querying interface, but a more complex Buffer Pool Manager, and file management. Also, **this project requires python 3.X**.

**Another Important Note:** We have taken a few shortcuts in this code to simplify it, which unfortunately means that there may be important synchronization failures we missed. Let me know if you see any unexpected behavior.


#### Synchronization in Python
Although you won't need to do any synchronization-related coding, it would be necessary for you to understand the basic Python synchronization primitives. The manual
explains this quite well: [https://docs.python.org/3/library/threading.html](High-level Threading Interface in Python). Some basics:
- Each transaction for us will be started in a sepearate thread (see `testingLock.py` for some examples). The main command for doing so is: `threading.Thread`, which takes a function name as an argument.
- The main synchronization primitives are: `Lock` and `RLock` (Sections 16.2.2 and 16.2.3 in the manual above). You create them by calling `threading.Lock()` or `threading.RLock()`, and you use them by acquiring and releasing them. Only one thread can take a Lock or a RLock at any time.
- Two other primitives build on top of the above: `Conditions` and `Events`. See the manual for the details on those. We use `Conditions` in `transactions.py` to signal threads.
- Using `with` simplifies this: a Lock/RLock/Condition/Event is passed as an argument, and only one thread can be in the body of the `with`.

## Files

#### `disk_relations.py` 
A `Relation` is backed by a file in the file system, i.e., all the data in the relation is written to a file and is read from a file. If a Relation is created with a non-existing fileName, then a new Relation is created with pre-populated 100 tuples. The file is an ASCII file -- the reading and writing is using `json` module. 

You can open the `relation1` file and see it's contents. The file is logically divided into blocks. The first block defines the column names, specifies the number of data blocks following, and gives a simple index (implemented as a hash). The index maps primary key values (always the first attribute) to blocks. Following this block are the blocks containing the tuples.

Relation files are opened at startup and *only* the first block is read. This
provides to the db column names, the number of disk blocks, and the index. The
file is then closed. When a tuple is later accessed the index is used to map
the tuple to a block, and the relation file is reopened and only that block is read.

`disk_relations.py` also contains a LRU Buffer Pool Implementation, with a fixed size Buffer Pool. 

#### `transactions.py`

This contains the implementaion of the Lock Table, and a Log Manager. Some details:
- `class LockTable`: This class implements a standard hash-based lock table. Object names are used as the identifiers for locking (so `objectid`s must be unique across all  
relations and tuples). **The code here and elsewhere implicitly assumes that there is a single relation in the database.** For each such object name, we keep track of the transations that currently have the lock (at most one in case of X locks), and a list of transactions that are waiting for a lock. 
- To avoid starvation: if T1 wants an S lock and T2 currently has one on that object, but T3 is waiting (say because it wants an X lock), we make T1 also wait, even though the locks would be compatible.
- `class LogManager`: This should be relatively straightforward. The transactions create log records (see below). `revertChanges` undoes a transaction in case of aborts. You can use Transaction4 (in `exampleTransactions.py`) to test this.
- `class TransactionManager`: manages the currently running transactions, basically doing some bookkeeping.
- `class TransactionState`: This class encapsulates some of the basic functionality of transactions, including some helper functions to create log records, keeping track of 
what locks the transaction currently holds, etc.


#### Development

There are two testing files, `testingLocks.py` and `testingRecovery.py` ("testingX" means both), one for working
w/ locks and one for recover.

Both contain code for testing. Running `python3 testingLocks.py` should get you
started. Note that the first time you run it, it will create the two files `relation1` and
`logfile`, but after you kill it, the logfile will be inconsistent (we never write out
CHECKPOINT records in normal course). So the second time you run it, it will error out
since the restartRecovery code is not implemented. So if you want to work on the other two
tasks, you should remove those two files every time.

Currently the only way to stop a runaway `testingX` is through killing it through Ctrl-C. If that doesn't work, try stopping it (Ctrl-Z), and then killing it using `kill %1`.

### Your Tasks

Your task is to finish a few of the unfinished pieces  in `transactions.py` (search for
**TO BE IMPLEMENTED**). 

* [10 points] Implementing IX Locks in `transactions.py`: Currently the code supports S, X, and IS locks. So if a transaction needs to lock a tuple in the X mode, the entire relation 
is locked. This
is of course not ideal and we would prefer to use IX locks (on the relation) to speed up concurrency. The code for this will largely mirror the code for IS. You will 
have to change the `getXLockTuple()` function and also the `compatibility_list` appropriately. 
* [20 points] Function `restartRecovery()` in `transaction.py`: This function is called if
  the log file indicates an inconsistency (i.e., if the logfile does not end with an empty
  CHECKPOINT record). If that's the case, then you must analyze the logfile and do a
  recovery on that. See 16.4.2 for details, though:
  * Our CLR records have a different format (see example logfiles for
    details), and
  * The book says to undo incomplete transactions in reverse order of their
    start records. You should
    undo tranactions *in the order they appear in the original log*, as shown
    in the slides. The order that the transactions are undone does not matter,
    as we have 2PL. There will never be more than a single incomplete
    transaction that modifies a given record.
	The individual operations of a single transaction, of course, are
    a different matter.

For the recovery, you will need to write the code for both `revertChanges` and `restartRecovery`. `revertChanges` works by writing a compensating log
record (CLR) for each update that a failed transaction does, in the correct
order. See `recoverytests-original` for examples of the format.

"Redo"-ing a transaction does not add any new log records, but it does modify
the database. 

Note that modifying the database a la `tup.setAttribute()` modifies the in-memory copy of the tuple, but does not push it to disk. You need to ensure that all such tuples make it to disk before adding the checkpoint record to the log.

### Testing

**Locks**
For locking, you should verify that your IX locks are working as intended. For **example**, you should ensure that:
- distinct tuples can be simultaneously locked *exclusively* by different transactions
- a tuple locked exclusively prevents a *shared* lock on the entire table.

You can use `testingLocks.py` as the basis for your testing. The provided version will create three transactions that contend for the same lock (on the entire relation) and pause for differing amounts of time. Running `python3 testingLocks.py` should produce something like:

        hub:~/project5> python3 testingLocks.py
        Transaction 1 able to         get this lock on relation1
        Transaction 1 able to get this lock on 20
        Transaction 2: compatible so able to get this lock on relation1
        Transaction 2 able to get this lock on 30
        Transaction 3: compatible so able to get this lock on relation1
        Transaction 3 able to get this lock on 40
        Transaction 3: Releasing lock on 40
        Transaction 3: Releasing lock on relation1
        Transaction 2: Releasing lock on 30
        Transaction 2: Releasing lock on relation1
        Transaction 1: Releasing lock on 20
        Transaction 1: Releasing lock on relation1
        hub:~/project5> 

Note that you should modify this test (change the transaction, or create a new one) such that it tests tuple locks as discussed above. This test works fine w/ tuple locks defaulting to table locks, but our tests will not.

We will test locks by running transactions that delay through `sleep`s and use timing
effects to ensure that your locks are conflicting when necessary, and not when not. We
will also check for the lock messages ("able to get this lock on...", etc.).


**Recovery**
Our testing will check both the contents of the database (the final versions of
the relation file) and the `logfile`.

Note that `testingRecovery.py` now uses **"relation"** instead of the original "relation1".

Example logs and relations are
in `recoverytests-original/` and `recoverytests-answers/`. Copy them into the
current directory to run, as in:

        titan:~/p5> cp recoverytests-original/recoverytest1_logfile logfile
        titan:~/p5> cp recoverytests-original/recoverytest1_relation relation
        titan:~/p5> cat logfile
        [1, "START"]
        [2, "START"]
        [3, "START"]
        [4, "START"]
        [5, "START"]
        [6, "START"]
        [5, "UPDATE", "recoverytest1_relation", "2", "A", "10", "7"]
        [5, "UPDATE", "recoverytest1_relation", "21", "A", "10", "13"]
        [4, "UPDATE", "recoverytest1_relation", "1", "A", "10", "7"]
        [4, "UPDATE", "recoverytest1_relation", "11", "A", "10", "13"]
        [6, "UPDATE", "recoverytest1_relation", "3", "A", "10", "7"]
        [6, "UPDATE", "recoverytest1_relation", "31", "A", "10", "13"]
        [5, "COMMIT"]
        [4, "CLR", "recoverytest1_relation", "11", "A", "10"]
        [6, "CLR", "recoverytest1_relation", "31", "A", "10"]
        [4, "CLR", "recoverytest1_relation", "1", "A", "10"]
        [4, "ABORT"]
        [6, "CLR", "recoverytest1_relation", "3", "A", "10"]
        [6, "ABORT"]
        [1, "UPDATE", "recoverytest1_relation", "0", "A", "10", "20"]
        [2, "UPDATE", "recoverytest1_relation", "10", "A", "10", "20"]
        [3, "UPDATE", "recoverytest1_relation", "20", "A", "10", "20"]
        [1, "COMMIT"]
        [2, "COMMIT"]
        [3, "COMMIT"]
        titan:~/p5> python testingRecovery.py 
        Reading from 'logfile' and 'relation'
        
        Setting the last_tranasction_id to be 6
        Starting Restart Recovery.......
        titan:~/p5> cat logfile 
        [1, "START"]
        [2, "START"]
        [3, "START"]
        [4, "START"]
        [5, "START"]
        [6, "START"]
        [5, "UPDATE", "recoverytest1_relation", "2", "A", "10", "7"]
        [5, "UPDATE", "recoverytest1_relation", "21", "A", "10", "13"]
        [4, "UPDATE", "recoverytest1_relation", "1", "A", "10", "7"]
        [4, "UPDATE", "recoverytest1_relation", "11", "A", "10", "13"]
        [6, "UPDATE", "recoverytest1_relation", "3", "A", "10", "7"]
        [6, "UPDATE", "recoverytest1_relation", "31", "A", "10", "13"]
        [5, "COMMIT"]
        [4, "CLR", "recoverytest1_relation", "11", "A", "10"]
        [6, "CLR", "recoverytest1_relation", "31", "A", "10"]
        [4, "CLR", "recoverytest1_relation", "1", "A", "10"]
        [4, "ABORT"]
        [6, "CLR", "recoverytest1_relation", "3", "A", "10"]
        [6, "ABORT"]
        [1, "UPDATE", "recoverytest1_relation", "0", "A", "10", "20"]
        [2, "UPDATE", "recoverytest1_relation", "10", "A", "10", "20"]
        [3, "UPDATE", "recoverytest1_relation", "20", "A", "10", "20"]
        [1, "COMMIT"]
        [2, "COMMIT"]
        [3, "COMMIT"]
        [-1, "CHECKPOINT", []]
        titan:~/p5> 

### Submission

We will test your functionality in a (partially) automated fashion, using a set of test cases. You should only need to change `transactions.py`. Submit your modified `transactions.py` file [here](https://umd.instructure.com/courses/1267269/assignments/4983021).
