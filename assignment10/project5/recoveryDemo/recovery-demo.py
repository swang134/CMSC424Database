from disk_relations import *
from transactions import *
import time
from exampletransactions import *
import sys
import subprocess
import random
import traceback
import shutil

os.remove("recoverydemo_logfile") if os.path.exists("recoverydemo_logfile") else None
os.remove("generated_relation") if os.path.exists("generated_relation") else None

bpool = BufferPool()
relationname = "generated_relation"
logfile = "recoverydemo_logfile"
orig_logfile = "recoverydemo_logfile_original"
shutil.copy(orig_logfile, logfile)
r = Relation(relationname)

#orig_relat = open(relationname, 'r')
#orig_relat_data = orig_relat.read()
#orig_relat.close()

print "Starting to analyze the logfile " + logfile
LogManager.setAndAnalyzeLogFile(logfile)
# print "Changes to the relations:"
# rel1 = orig_relat_data
# rel2 = open(relationname, 'r').read()
#
# diff1 = ""
# diff2 = ""
# for i in range(Globals.blockSize, max(len(rel1), len(rel2))):
# 	if rel1[i] != rel2[i]:
# 		diff1 += rel1[i]
# 		diff2 += rel2[i]

#print "-- Original Relation: " + diff1
#print "-- Relation after recovery: " + diff2

print "Comparing the logfiles"
print "-- Original Logfile: "
print open(orig_logfile, 'r').read()
print "-- Logfile after recovery: "
print open(logfile, 'r').read()
