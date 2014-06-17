def record(filename, dct):
    fout = open(filename, "a")
    
    lst=dct.keys()
    if(lst is None):
        return
    if(len(lst)==0 and lst):
        return
    for key in lst:
        print >>fout, key, ":", dct[key], "|",
    print >>fout, ''
    print dct
    fout.close()