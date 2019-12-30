import time
def read_value(string):
    if string[0] == "'" and string[-1] == "'":
        return string[1:-1]
    val = string
    try:
        val = int(string)
    except:
        try:
            val = float(string)
        except:
            pass
    return val

def load_options(fname):
    d_options = {}
    f = open(fname, "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        ignore = 0
        if (len(line) > 0):
            if line[0] == "#":
                ignore = 1
        if (ignore == 0 and "\t" in line):
            line = line[:-1]
            li = line.split("\t")
            d_options[li[0]] = read_value(li[1])
    return d_options

def flog(msg, fname):
    f = open(fname, "a+")
    f.write(repr(time.time()) + "\t" + str(msg) + "\n")
    f.close()

def flog(msg, fname, logtime=0):
    f = open(fname, "a")
    if logtime == 0:
        f.write(str(msg) + "\n")
    if logtime == 1:
        f.write(repr(time.time()) + "\t" + str(msg) + "\n")
    f.close()
   

def get_list(d):
    #replaces gen_list.py, load_listn, load_list. Use load_data_from_list on this output to get data.
    #returns train_list, test_list, where train_list[i] are the filenames of class i.
    #train_list[cend] are the filenames of the open class, if any. (OPEN_INSTNUM = 0 explicitly defines no open class)
    #get cstart, cend, ostart, oend. two ways to do so: with or without an explicit start.

    if "TRAIN_CINSTNUM" in d.keys():
        return get_list_with_sizes(d) #divert to other function
    
    if "CLOSED_SITESTART" in d.keys():
        cstart = d["CLOSED_SITESTART"]
        cend = d["CLOSED_SITEEND"]
    else:
        cstart = 0
        cend = d["CLOSED_SITENUM"]

    if "OPEN_INSTSTART" in d.keys():
        ostart = d["OPEN_INSTSTART"]
        oend = d["OPEN_INSTEND"]
    else:
        ostart = 0
        oend = d["OPEN_INSTNUM"]

    reqs = ["CLOSED_INSTNUM", "DATA_LOC", "FOLD_MODE", "FOLD_NUM", "DATA_TYPE"]
    for req in reqs:
        if not req in d.keys():
            raise Exception("{} not found in options.".format(req))

    iend = d["CLOSED_INSTNUM"]

    #default 10-fold. (Not much reason to change this.)

    if ("FOLD_TOTAL" in d):
        foldtotal = d["FOLD_TOTAL"]
    else:
        foldtotal = 10

    train_list = []
    test_list = []
    for i in range(cend):
        train_list.append([])
        test_list.append([])
    if oend != 0:
        train_list.append([])
        test_list.append([])

    #different modes
    #MODE 2: trainlist = testlist, according to parameters
    #MODE 3: standard X-fold. trainlist != testlist: testlist is fold ~X, trainlist is fold X (len(testlist) << len(trainlist))
    #MODE 4: trainlist != testlist: testlist is fold X, trainlist is fold X+1 (len(trainlist) == len(testlist))
        #for final set, testlist is fold X+1, trainlist is fold X

    if (d["FOLD_MODE"] == 2):
        for s in range(cstart, cend):
            for i in range(0, iend):
                sname = d["DATA_LOC"] + str(s) + "-" + str(i) + "." + d["DATA_TYPE"]
                train_list[s].append(sname)
                test_list[s].append(sname)
        for s in range(ostart, oend):
            sname = d["DATA_LOC"] + str(s) + "." + d["DATA_TYPE"]
            train_list[-1].append(sname)
            test_list[-1].append(sname)

    if (d["FOLD_MODE"] == 3):
        for s in range(cstart, cend):
            for i in range(0, iend):
                sname = d["DATA_LOC"] + str(s) + "-" + str(i) + "." + d["DATA_TYPE"]
                if (i >= d["CLOSED_INSTNUM"]/foldtotal * d["FOLD_NUM"] and
                    i < d["CLOSED_INSTNUM"]/foldtotal * (d["FOLD_NUM"]+1)):
                    test_list[s].append(sname)
                else:
                    train_list[s].append(sname)
        for s in range(ostart, oend):
            sname = d["DATA_LOC"] + str(s) + "." + d["DATA_TYPE"]
            if (s >= (oend-ostart)/foldtotal * d["FOLD_NUM"] + ostart and
                s < (oend-ostart)/foldtotal * (d["FOLD_NUM"]+1) + ostart):
                test_list[-1].append(sname)
            else:
                train_list[-1].append(sname)

    if (d["FOLD_MODE"] == 4):
        for s in range(cstart, cend):
            for i in range(0, iend):
                sname = d["DATA_LOC"] + str(s) + "-" + str(i) + "." + d["DATA_TYPE"]
                if (i >= d["CLOSED_INSTNUM"]/foldtotal * d["FOLD_NUM"] and
                    i < d["CLOSED_INSTNUM"]/foldtotal * (d["FOLD_NUM"]+1)):
                    test_list[s].append(sname)
        for s in range(ostart, oend):
            sname = d["DATA_LOC"] + str(s) + "." + d["DATA_TYPE"]
            if (s >= (oend-ostart)/foldtotal * d["FOLD_NUM"] + ostart and
                s < (oend-ostart)/foldtotal * (d["FOLD_NUM"]+1) + ostart):
                test_list[-1].append(sname)
        trainfoldnum = d["FOLD_NUM"] + 1
        if trainfoldnum >= foldtotal:
            trainfoldnum = d["FOLD_NUM"] - 1
        for s in range(cstart, cend):
            for i in range(0, d["CLOSED_INSTNUM"]):
                sname = d["DATA_LOC"] + str(s) + "-" + str(i) + "." + d["DATA_TYPE"]
                if (i >= d["CLOSED_INSTNUM"]/foldtotal * trainfoldnum and
                    i < d["CLOSED_INSTNUM"]/foldtotal * (trainfoldnum+1)):
                    train_list[s].append(sname)
        for s in range(ostart, oend):
            sname = d["DATA_LOC"] + str(s) + "." + d["DATA_TYPE"]
            if (s >= (oend-ostart)/foldtotal * trainfoldnum + ostart and
                s < (oend-ostart)/foldtotal * (trainfoldnum+1) + ostart):
                train_list[-1].append(sname)

    return train_list, test_list
   
def get_list_with_sizes(d):
    #instead of using fold mode, this uses specific sizes to return train_list and test_list:
    #TRAIN_CINST_NUM (TRCN), TRAIN_OINST_NUM (TRON), TEST_CINST_NUM (TECN), TEST_OINST_NUM (TEON),
    #START_CINST_NUM (STCN), START_OINST_NUM (STON)
    #the test_inst always follow the train_inst if RE = 1 or otherwise if RE = -1
    #(So this currently cannot be used to implement 10-fold testing.)

    #e.g. if the above are 20, 2000, 30, 3000, 50, 0, then instances 50-70 are training and 70-100 are testing

    TRCN = d["TRAIN_CINSTNUM"]
    TRON = d["TRAIN_OINSTNUM"]
    TECN = d["TEST_CINSTNUM"]
    TEON = d["TEST_OINSTNUM"]
    STCN = d["START_CINSTNUM"]
    STON = d["START_OINSTNUM"]
    SN = d["CLOSED_SITENUM"]
    CN = d["CLOSED_INSTNUM"]
    ON = d["OPEN_INSTNUM"]
    RE = d["TRAIN_FIRST"]

    if RE == -1:
        #we are going to pretend the train list is the test list
        #for this to work, we need to reverse train/test numbers now
        TECN = d["TRAIN_CINSTNUM"]
        TEON = d["TRAIN_OINSTNUM"]
        TRCN = d["TEST_CINSTNUM"]
        TRON = d["TEST_OINSTNUM"]

    assert(TRCN + TECN + STCN <= CN)
    assert(TRON + TEON + STON <= ON)

    train_list = []
    test_list = []
    for i in range(SN):
        train_list.append([])
        test_list.append([])
    if ON != 0:
        train_list.append([])
        test_list.append([])

    for s in range(SN):
        for i in range(CN):
            sname = d["DATA_LOC"] + str(s) + "-" + str(i) + "." + d["DATA_TYPE"]
            if i >= STCN and i < STCN + TRCN:
                train_list[s].append(sname)
            elif i >= STCN + TRCN and i < STCN + TRCN + TECN:
                test_list[s].append(sname)
    for s in range(ON):
        sname = d["DATA_LOC"] + str(s) + "." + d["DATA_TYPE"]
        if s >= STON and s < STON + TRON:
            train_list[-1].append(sname)
        elif s >= STON + TRON and s < STON + TRON + TEON:
            test_list[-1].append(sname)

    if RE == 1:
        return train_list, test_list
    else:
        return test_list, train_list


