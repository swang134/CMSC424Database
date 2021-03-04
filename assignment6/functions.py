import json
import re
from pyspark import SparkContext

# A hack to avoid having to pass 'sc' around
dummyrdd = None
def setDefaultAnswer(rdd):
	global dummyrdd
	dummyrdd = rdd

def task1(amazonInputRDD):
        return dummyrdd

def task2_flatmap(x):
        return []
        
def task3(logsRDD, l):
        return dummyrdd

def task4(logsRDD, day1, day2):
        return dummyrdd

def task5(playRDD):
        return dummyrdd

def task6(bipartiteGraphRDD, currentMatching):
        return dummyrdd
