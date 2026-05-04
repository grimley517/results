import os

dirs = ("Autumn","blackaby","caulcott","fastnet","houghton","Icicle","portland","rockall","shortCourse1","shortCourse2","shortCourse3","shortCourse4","Watts","wednesday")
sailors = set()
sailorsD = {}
for d in dirs:
    for f in os.listdir(d):
        if f.endswith(".race"):
            file = open(d+"/"+f)
            line = file.readline()
            while(not ("<HANDICAPS>" in line)): 
                line = file.readline()
                toks = line.split(",")
                if len(toks) >3:
                    sailor = toks[1]
                    sailors.add(sailor)
                    if sailor in sailorsD.keys():
                        sailorsD[sailor] += 1
                    else:
                        sailorsD[sailor] = 1


for s in sorted(sailorsD, key=sailorsD.get,reverse=True):
    print(s,sailorsD[s])
