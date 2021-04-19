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
os.remove("logfile") if os.path.exists("logfile") else None
os.remove("relation1") if os.path.exists("relation1") else None

bpool = BufferPool()
r = Relation('relation1')
LogManager.setAndAnalyzeLogFile('logfile')

# Start the transactions
def testingone():
	stime = 8
	for primary_id in ["20", "30", "40"]:
		t = threading.Thread(target=Transaction1, args=(r, primary_id, stime))
		t.start()
		stime = stime / 2

testingone()


### Wait for all the threads to complete
main_thread = threading.currentThread()
for t in threading.enumerate():
	if t is not main_thread:
		t.join()
BufferPool.writeAllToDisk(r)
