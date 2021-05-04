## Assignment 11: Transactions, Due May 9, 2021

*The assignment is to be done by yourself.*

*Although we have provided a Vagrantfile as usual, you only really need python3 for this assignment.*


### Overview

In this assignment you will modify our simple database to emulate first-committer *snapshot
isolation* instead of lock-based two-phase consistency.

Snapshot isolation is usually implemented using a *multi-versioned* database;
snapshot reads can be done at any time by specifying older timestamps. We do
not have a multi-versioned database, so instead we will handle snapshot reads
by specifying the readset and writeset ahead of time, and *stashing* a snapshot of the
relevant data. Note that this technique is also used in some high-performance
distributed databases<sup>1</sup>. Subsequent reads by the transaction will read from the stashed
copies, rather than directly from the database.

Writes in snapshot isolation are buffered, and only pushed to the database
when the transaction *validates*, i.e. is guaranteed to succeed. A transaction *i*
validates if and only if no other transaction commits between the time *i*
starts and attempts to validate. This is straightforward in a multi-versioned
database which, again, we do not have. We will emulate this by allowing *i* to validate if none of
the items in its writeset change values during the course of *i*'s execution.
This essentially means that (1) we also stash all data in the writeset at the
start of transaction execution, and (2) we compare the stashed value w/ the
"current" value at commit time to see if it has changed.

Transactions that fail validation are aborted.

Note that in a real database validation and commitment should be a single
atomic action; we will not go that far in this system. The example
transactions should never execute their transactions close enough together for
this discrepancy to be apparent.

### Details.

- Snapshot isolation requires reads to be satisfied by the snapshot of the db at
transaction start. Define `takeSnapshot()` to save copies of the data items
named in the readset. 
- In order to ensure that reads see the snapshot we define new `getAttribute()` and
  `setAttribute()` methods directly on transaction state, rather directly
  on the corresponding disk functions as used before. This only affects the
  methods in `exampleTransactions.pl`, so it should be transparent to you.
- You will have to define (at least logically) three new pieces of transaction
  state: the *snapshot*, a *write-buffer*, and a *writeset* (though this last
  can be derived from the contents of the write-buffer.
- Validation is done during transaction commit. Call `abortTransaction()` and
  return if it fails. Push write-buffer contents to the database if it passes. 

As in prior assignments, you will only have to write a small amount of
code. Your changes will be confined to `transactions.py`, and *only* that file
should be uploaded to gradescope.  Search for "SNAPSHOT_ISO" or "YOUR CODE
HERE" to find places that need to be modified.

Use `python3 testing.py` to test your implementation locally prior to
gradescope submission.

### Submission
You should submit modified `transactions.py` file to [Gradescope](https://www.gradescope.com/courses/219072/assignments/914016/submissions). 

You should not need to change anything any other files.

### Notes

<sup>1</sup>Thomson, A., Diamond, T., Weng, S. C., Ren, K., Shao, P., & Abadi, D. J. "Calvin: fast distributed transactions for partitioned database systems." *Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data*. 2012.

