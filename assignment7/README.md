## Project 7: Indexes

*The assignment is to be done by yourself.*

*If you have Python 3 running on your machine, you should be able to just use that -- you don't need to set up Vagrant for this assignment.*

### Overview

In this project, you will modify a very simple database system that we have written to illustrate some of the B+-Tree algorithms. 
The database system is written in Python and attempts to simulate how a database system would work, including what blocks it would read from disk, etc.

* `disk_relations.py`: This module contains the classes Block, RelationBlock, Relation, and a few others helper classes like Pointer. A Block is a base class, 
that is subclassed by RelationBlock and BTreeBlock (in `btree.py` file). A RelationBlock contains a set of tuples, and a Relation contains a list of RelationBlocks. 
* `btree.py`: Code that implements some of the BTree functionality including search, insert, and delete (partially). The main class here is the BTreeBlock class, that captures the information stored in a BTree node.

There are a set of parameters that control how many tuples can be stored in each RelationBlock, how many key/ptrs can be stored in each BTreeBlock, etc. You can't set those directly, but you can set the "blockSize" and also the size of a key, etc. Those parameters are in the class `Globals`, and can be modified to constructs trees of different fanouts.

**Important Note: The B+-Tree code isn't fully debugged and there may be corner cases where it fails. Let us know if you see unexpected behavior.**

### How to Use the Files

The directory also contains two other files:
* `create_sample_databases.py`: Creates a sample database with 2 relations and 2 indexes.
* `testing-btree.py`: Shows the execution of some simple btree tasks using the sample data. 

The simplest way you can run this is by just doing: `python testing-btree.py`
That will run all the code in the `testing-btree.py` file.

A better option is to do: `python -i testing-btree.py`. This will execute all the code in `testing-btree.py` file and then it will open a Python shell. In that shell, you can start doing more operations (e.g., you can play with the index to add/delete tuples, etc.)

### Your Task

Your task is to finish one unfinished piece in the `btree.py` file.

* Function `redistributeWithBlock(self, otherBlock)` in `btree.py`: The delete code does not handle the case where an underfull node borrows entries from one of its siblings.

You are to implement this function. **Note that `redistributeWithBlock` is called on the right child for this project.** Refer to Figure 11.19 in the textbook for guidance. You will need to cover 4 cases:
* When the right (self) child is underful and (1) it's a leaf node and (2) it's not a leaf node
* When the left (other) child is underful and (3) it's a leaf node and (4) it's not a leaf node

Note that you only need to return the value that will update kprime.

### Submission
You should submit modified `btree.py` file. We will test those in an automated fashion, using a set of test cases (on Gradescope).
