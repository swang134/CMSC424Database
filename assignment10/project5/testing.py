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
LogManager.setAndAnalyzeLogFile('logfile')

# Start the transactions
def testingone():
	stime = 8
	for primary_id in ["20", "30", "40"]:
		t = threading.Thread(target=Transaction1, args=(r, primary_id, stime))
		t.start()
		stime = stime / 2

def testingabort():
	t = threading.Thread(target=Transaction4, args=(r, "0", "10", 2, True))
	t.start()

testingone()
#testingabort()

### Wait for all the threads to complete
main_thread = threading.currentThread()
for t in threading.enumerate():
	if t is not main_thread:
		t.join()
BufferPool.writeAllToDisk(r)
