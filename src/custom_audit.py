#!/usr/bin/python3
import os
import datetime
import json

handicaps,QEfile = json.loads(open("config.json","r").read())

audits = []

class Race:
    def __init__(self):
        self.entries = []

    def datum(self):
        avg = 0
        datum = 0
        for e in self.entries:
            avg += e.corrected
        avg /= len(self.entries)
        cutoff = 1.05*avg
        valid = 0
        for e in self.entries:
            if e.corrected < cutoff:
                valid += 1
                datum += e.corrected
        datum = datum/valid
        return datum

class Entry:
    def __init__(self,qe,py,laps,time):
        self.corrected = time*1000/laps/py
        self.QE = qe

    def audit(self,avg):
        return int(self.corrected / avg * 1000)

PYcols = {'CLASS': 0, 'PY': 1,'TYPE': 2, 'RIG': 3, 'CREW': 4, 'KITE': 5}
QEcols = {'QE': 0, 'HELM': 1, 'CREW': 2, 'CLASS': 3, 'SAILNO': 4, 'PERSONAL': 5, 'AGEGROUP': 6, 'FLEET': 7}
raceEntryCols = {'QE': 0, 'HELM': 1, 'CREW': 2, 'CLASS': 3, 'SAILNO': 4, 'TIME': 5, 'LAPS': 6, 'FINCODE': 7, 'what':8}

QES = []
Classes = []
PYs = dict()

fleets = ["G", "S"]
ageGroups = ["J", "S", "M", "G"]

for line in open(handicaps, "r").readlines():
    tokens = line.split(",")
    if tokens[0] != "":
        Classes.append(tokens[PYcols['CLASS']])
        PYs[tokens[PYcols['CLASS']]] = (int(tokens[PYcols['PY']]))
retiredQEs = []

for line in open("retiredQEs.txt", "r").readlines():
    retiredQEs.append(line.split(",")[0])
#parses and verify QES
for line in open(QEfile, "r").readlines():
   line = line.replace('\r', '')
   line = line.replace('\n', '')
   tokens = line.split(",")

   if len(tokens) == len(QEcols):
        if tokens[QEcols['CLASS']] in Classes:
            if tokens[QEcols['AGEGROUP']] in ageGroups:
                if tokens[QEcols['FLEET']] in fleets:
                    try:
                        int(tokens[QEcols['PERSONAL']])
                        QES.append([tokens[QEcols['QE']],
                                    int(tokens[QEcols['PERSONAL']]),
                                    [],
                                    tokens])
                    except:
                        print("ERROR:", line, "personal is not a number", tokens[QEcols['PERSONAL']])
                else:
                    print("ERROR:" , line, "unknown fleet", "'" + tokens[QEcols['FLEET']] + "'")
            else:
                print("ERROR:", line, "unknown age group")
        else:
            print("ERROR:", line, "unknown class", tokens[QEcols['CLASS']])


   elif len(tokens) != 1:
       print("ERROR:", line, "\n should have 7 tokens QE,HELM,CREW,CLASS,SAILNO,PERSONAL,AGERGROUP, Contains:", len(tokens))


name = "icicle"

files = os.listdir(name)
for f in files:
    if f[-5:] == ".race":
        race = Race()
        #print(f)
        for e,line in enumerate(open(f"{name}/{f}","r").readlines()[1:]):
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            if line == "<HANDICAPS>":
                break
            else:
                tokens = line.split(",")
                if len(tokens) == len(raceEntryCols):
                    qe = tokens[raceEntryCols['QE']]
                    valid = False
                    #if not(qe in [item[0] for item in QES]) and not(qe in retiredQEs):
                        #print(f"Warning: File:{f} Line: {e} QE: {qe}")
                    for QE in QES:
                        if qe == QE[0]:
                            valid = True

                    if valid & (tokens[raceEntryCols['FINCODE']] == ""):
                        try:
                            py = int(PYs[tokens[raceEntryCols['CLASS']]])
                            laps = int(tokens[raceEntryCols['LAPS']])
                            time = int(tokens[raceEntryCols['TIME']])
                            race.entries.append(Entry(qe, py, laps, time))
                        except:
                            print("WARNING:", line, "in file: ", f, "PY, LAPS & TIME must all be integers")
                else:
                    if not (",,,,,,," in line):
                        print("WARNING:", line, "in file: ", f, "unknown QE")
        if len(race.entries) > 1:
            datum = race.datum()
            for e in race.entries:
                for qe in QES:
                    if qe[0] == e.QE:
                        qe[2].append(e.audit(datum))
                if e.QE == "RH400SB":
                    rn = int(f.split(" ")[1])
                    audits.append((rn,f,e.audit(datum)))

for rn,f,n in (sorted(audits, key=lambda x: x[0])):
    print(f,n)
