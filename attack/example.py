import sys
from  loaders import *
import time
#load options
try:
    optfname = sys.argv[1]
    d = load_options(optfname)
except Exception,e:
    print sys.argv[0], str(e)
    sys.exit(0)

#ready to log info
ofname = "{}{}-{}".format(d["OUTPUT_LOC"], "Test", d["CORE_NAME"])
logfname = ofname + ".log"
flog(sys.argv[0] + " " + sys.argv[1], logfname, logtime=1)
flog(repr(d), logfname)

#get alll names from data
atrainnames, atestnames = get_list(d)
#unpack trainnames, testnames
trainnames = [name for tname in atrainnames for name in tname]
testnames = [name for tname in atestnames for name in tname]

print trainnames[0:10]


