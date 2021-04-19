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

print("Reading from '{}' and '{}'\n".format("logfile", "relation"))
bpool = BufferPool()
r = Relation('relation')
LogManager.setAndAnalyzeLogFile('logfile')

