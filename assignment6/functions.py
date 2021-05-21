import json
import re
from pyspark import SparkContext

# A hack to avoid having to pass 'sc' around
dummyrdd = None
def setDefaultAnswer(rdd):
	global dummyrdd
	dummyrdd = rdd

def task1(amazonInputRDD):
        PRDD= amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], 1 if float(x[2])==1.0 else 0))
        CRDD = PRDD.mapValues(lambda v: (v, 1)).reduceByKey(lambda a,b: (a[0]+b[0], a[1]+b[1])).mapValues(lambda v: v[0]/v[1]) 
        return CRDD

def task2_flatmap(x):
        NRDD = []
        for i in range(0, len(x['laureates'])):
                NRDD.append(x['laureates'][i]['surname']) 
        return NRDD
        
def task3(logsRDD, l):
        LRDD= logsRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0] if x[3][1:12] in l[0] else "", x[3][1:12])).filter(lambda x: x[0] != "").distinct()
        for i in range(1,len(l)): 
                RDD = logsRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0] if x[3][1:12] in l[i] else "", x[3][1:12])).filter(lambda x: x[0] != "").distinct()
                LRDD = LRDD.join(RDD)
        AnswerRDD = LRDD.map(lambda x: x[0])
        return AnswerRDD

def task4(logsRDD, day1, day2):
        Day1RDD = logsRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0] if x[3][1:12] in day1 else "", x[6])).filter(lambda x: x[0] != "")
        Day2RDD = logsRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0] if x[3][1:12] in day2 else "", x[6])).filter(lambda x: x[0] != "")
        Day1 = Day1RDD.reduceByKey(lambda a, b: a + ',  ! '+ b).map(lambda x: (x[0], list(x[1].split(",  ! "))))
        Day2 = Day2RDD.reduceByKey(lambda a, b: a + ',  ! '+ b).map(lambda x: (x[0], list(x[1].split(",  ! "))))
        Day = Day1.join(Day2)
        return Day

def t5help(l): 
        Tlist = [] 
        for i in range(1,len(l)): 
                Tlist.append((l[i-1],l[i]))
        return Tlist

def task5(playRDD):
        RRDD = playRDD.map(lambda x: re.sub("\W", lambda ele: " " + ele[0] + " ", x)).map(lambda x: x.strip())
        CRDD = RRDD.map(lambda x: re.split('\s+', x)).map(lambda x: list(x))
        LRDD = CRDD.map(lambda x: t5help(x))
        count = LRDD.flatMap(lambda data: data).map(lambda w: (w,1)).reduceByKey(lambda a, b: a+b)
        return count

def task6(bipartiteGraphRDD, currentMatching):
        return dummyrdd

