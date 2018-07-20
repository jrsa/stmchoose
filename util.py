def printdict(d):
    for k in d:
        print("{}: {}".format(k, d[k]))
    print("{} total".format(len(d)))