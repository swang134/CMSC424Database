## CMSC424 Spring 2021 Assignment 6: Spark
### Due Mar 12, 2021, 11:59PM

Assignment 6 focuses on using Apache Spark for doing large-scale data analysis tasks. For this assignment, we will use relatively small datasets and  we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets.

## Getting Started with Spark

This guide is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes
the 2-stage Map-Reduce paradigm (originally proposed by Google and popularized by open-source Hadoop system); Spark is instead based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection
of items, that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as
chains of these operations.

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager.

### Installing Spark

As before, we have provided a VagrantFile in the `assignment6` directory. Since the Spark distribution is large, we ask you to download that directly from the Spark website.

1. Download the Spark package at https://archive.apache.org/dist/spark/spark-3.0.1/ (other downloads [here](https://spark.apache.org/downloads.html)). We will use **Version 3.0.1, Pre-built for Hadoop 2.7 or later**.
2. Move the downloaded file to the `assignment6/` directory (so it is available in '/vagrant' on the virtual machine), and uncompress it using:
`tar zxvf spark-3.0.1-bin-hadoop2.7.tgz` in your VM.
3. This will create a new directory: `spark-3.0.1-bin-hadoop2.7`.
4. (optional) This step is included in the VagrantFile, but if you get any error related to `$SPARKHOME`, you can set the variable with: <br> `export SPARKHOME=/vagrant/spark-3.0.1-bin-hadoop2.7` and then <br> `echo "export SPARKHOME=/vagrant/spark-3.0.1-bin-hadoop2.7" >> .bashrc`

We are ready to use Spark.

### Spark and Python

Spark primarily supports three languages: Scala (Spark is written in Scala), Java, and Python. We will use Python here -- you can follow the instructions at the tutorial
and quick start (http://spark.apache.org/docs/latest/quick-start.html) for other languages. The Java equivalent code can be very verbose and hard to follow. The below
shows a way to use the Python interface through the standard Python shell.

### Jupyter Notebook

To use Spark within the Jupyter Notebook (and to play with the Notebook we have provided), you can do (from the `/vagrant` directory on the VM):
	```
	PYSPARK_PYTHON=/usr/bin/python3 PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --ip=0.0.0.0 --port=8881" $SPARKHOME/bin/pyspark
	```
### PySpark Shell

You can also use the PySpark Shell directly.

1. `$SPARKHOME/bin/pyspark`: This will start a Python shell (it will also output a bunch of stuff about what Spark is doing). The relevant variables are initialized in this python
shell, but otherwise it is just a standard Python shell.

2. `>>> textFile = sc.textFile("README.md")`: This creates a new RDD, called `textFile`, by reading data from a local file. The `sc.textFile` commands create an RDD
containing one entry per line in the file.

3. You can see some information about the RDD by doing `textFile.count()` or `textFile.first()`, or `textFile.take(5)` (which prints an array containing 5 items from the RDD).

4. We recommend you follow the rest of the commands in the quick start guide (http://spark.apache.org/docs/latest/quick-start.html). Here we will simply do the Word Count
application.

#### Word Count Application

The following command (in the pyspark shell) does a word count, i.e., it counts the number of times each word appears in the file `README.md`. Use `counts.take(5)` to see the output.

`>>> counts = textFile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)`

Here is the same code without the use of `lambda` functions.

```
def split(line):
    return line.split(" ")
def generateone(word):
    return (word, 1)
def sum(a, b):
    return a + b

textfile.flatMap(split).map(generateone).reduceByKey(sum)
```

The `flatmap` splits each line into words, and the following `map` and `reduce` do the counting (we will discuss this in the class, but here is an excellent and detailed
description: [Hadoop Map-Reduce Tutorial](http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html#Source+Code) (look for Walk-Through).

The `lambda` representation is more compact and preferable, especially for small functions, but for large functions, it is better to separate out the definitions.

### Running it as an Application

Instead of using a shell, you can also write your code as a python file, and *submit* that to the spark cluster. The `assignment6` directory contains a python file `wordcount.py`,
which runs the program in a local mode. To run the program, do:
`$SPARKHOME/bin/spark-submit wordcount.py`

### More...

We encourage you to look at the [Spark Programming Guide](https://spark.apache.org/docs/latest/programming-guide.html) and play with the other RDD manipulation commands.
You should also try out the Scala and Java interfaces.

## Assignment Details

We have provided a Python file: `assignment.py`, that initializes the folllowing RDDs:
* An RDD consisting of lines from a Shakespeare play (`play.txt`)
* An RDD consisting of lines from a log file (`NASA_logs_sample.txt`)
* An RDD consisting of 2-tuples indicating user-product ratings from Amazon Dataset (`amazon-ratings.txt`)
* An RDD consisting of JSON documents pertaining to all the Noble Laureates over last few years (`prize.json`)

The file also contains some examples of operations on these RDDs.

Your tasks are to fill out the 5 functions that are defined in the `functions.py` file (starting with `task`). The amount of code that you write would typically be small (several would be one-liners), with the exception of the last one.

First 2 tasks are worth 0.5 points each, the following 2 tasks are worth 1 point each, and task 5 is worth 2 points.

- **Task 1**: This function takes as input the amazonInputRDD and calculate the proportion of 1.0 rating review out of all reviews made by each customer. The output will be an RDD where the key is the customer's user id, and the value is the proportion in decimal. This can be completed by using `aggregateByKey` or `reduceByKey` along with `map`.

- **Task 2**: Write just the flatmap function (`task2_flatmap`) that takes in a parsed JSON document (from `prize.json`) and returns the surnames of the Nobel Laureates. In other words, the following command should create an RDD with all the surnames. We will use `json.loads` to parse the JSONs (this is already done). Make sure to look at what it returns so you know how to access the information inside the parsed JSONs (these are basically nested dictionaries). (https://docs.python.org/2/library/json.html)
```
     	task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap)
```

- **Task 3**: This function operates on the `logsRDD`. It takes as input a list of *dates* and returns an RDD with "hosts" that were present in the log on all of
those dates. The dates would be provided as strings, in the same format that they appear in the logs (e.g., '01/Jul/1995' and '02/Jul/1995').
The format of the log entries should be self-explanatory, but here are more details if you need: [NASA Logs](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html)
Try to minimize the number of RDDs you end up creating.

- **Task 4**: On the `logsRDD`, for two given days (provided as input analogous to Task 9 above), use a 'cogroup' to create the following RDD: the key of
the RDD will be a host, and the value will be a 2-tuple, where the first element is a list of all URLs fetched from that host on the first day, and the second element
is the list of all URLs fetched from that host on the second day. Use `filter` to first create two RDDs from the input `logsRDD`.

- **Task 5**: NLP often needs to preprocess the input data and can benefit a lot from cluster computing. [Tokenization](https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization) is the process of chopping up the raw text. [Bigrams](http://en.wikipedia.org/wiki/Bigram) are sequences of two consecutive words. For example, the previous sentence contains the following bigrams: "Bigrams are", "are simply", "simply sequences", "sequences of", etc. Your task here is to tokenize each line in playRDD by first separating out any punctuation and then converting each segment separated by a space as a token (e.g. `Task 5: I'm easy.` will be tokenized into `["Task", "5", ":", "I", "'", "m", "easy", "."]`); and count the appearance of each bigram in the tokens. The return value should be a RDD where the key is a bigram, and the value is its count.

- **Task 6 (No Credit)**: [Maximal Matching] `task6` should implement one iteration of a greedy algorithm for finding a maximal matching in a bipartite graph.
A *matching* in a graph is a subset of the edges such that no two edges share a vertex (i.e., every vertex is part of at most 1 edge in the matching). A *maximal* matching
is such that, we cannot add any more edges to it (in other words, there is no remaining edge in the graph both of whose endpoints are unmatched). Here is a simple greedy
algorithm for finding a maximal matching using map-reduce; note that this is not a particularly good algorithm for solving this problem, but it is easy to parallelize.
We maintain the current state of the program in a PairRDD called currentMatching, where we note all the user-product relationships
that have already been chosen. Initially this RDD is set to be empty (for making it easy to debug, we have added one entry to it).
The following is then executed repeatadly till currentMatching does not change.
  * For each user who is currently unmatched (i.e., does not have an entry in currentMatching), find the group of products connected to it that are also unmatched.
  * For each such user, among the group of unmatched products it is connected to, pick the `min` (it is better to pick this randomly but then the output is not deterministic and will make testing/debugging difficult)
  * It is possible that we have picked the same product two different unmatched users, which would violate the matching constraint.
  * In another step, repeat the same process from the products' perspective, i.e., for each product that has been picked as potential match for multiple user nodes, pick the minimum user node (again doing this randomly is better).
  * Now we are left with a set of user-product relationships that we can add to currentMatching and iterate

### Sample results.txt File
You can use spark-submit to run the `assignment.py` file, but it would be easier to develop with `pyspark` (by copying the commands over).

**results.txt** shows the results of running assignment.py on our code using: `$SPARKHOME/bin/spark-submit assignment.py`

### Submission

Submit the `functions.py` file.
