#!/usr/bin/python3
import os
import datetime
import json

handicaps,QEfile = json.loads(open("config.json","r").read())

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



files = os.listdir("audit")
for f in files:
    if f[-5:] == ".race":
        race = Race()
        #print(f)
        for e,line in enumerate(open(f"audit/{f}","r").readlines()[1:]):
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            if line == "<HANDICAPS>":
                break
            else:
                tokens = line.split(",")
                if len(tokens) == len(raceEntryCols):
                    qe = tokens[raceEntryCols['QE']]
                    valid = False
                    if not(qe in [item[0] for item in QES]) and not(qe in retiredQEs):
                        print(f"Warning: File:{f} Line: {e} QE: {qe}")
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



html = f'''<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Stewartby Sailing Personal Handicaps</title>
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0, minimal-ui">
	<link rel="stylesheet" href="../styles.css">
	<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
	<meta name="description" content="personal handicaps.">

</head>
<body>
	<div class="section">

<div class="group align-centre">
			<div class="horizontal-wrapper">	
				<p class="label-medium on-surface-variant">Stewartby Sailing</p>
			</div>
			<h1 class="display-small on-surface">Personal Handicaps</h1>
            <p class="label-medium on-surface-variant">{str(datetime.date.today())}</p>
            </div>
<div class="divider"></div>

<div class="section">
<h2>How personal handicaps are calculated: </H2>
</div>
<div class="section">
For each race in a rolling years worth of races (including Wednesday evenings but not short course) all the Portsmouth Yardstick corrected times are averaged and multiplied by 1.05
to give a cut off time any times greater than this value are discarded, because they are most likely the result of someone having a really bad race so is not representative and will unduly influence the handicaps.
</div>

<div class="section">
<h2>Sample race:</h2>
<table><tr><th>Competitor</th><th>Corrected Time (s)</th></tr>
<tr><td>Ade</td><td>3000</td></tr>
<tr><td>Bob</td><td>3100</td></tr>
<tr><td>Carl</td><td>3200</td></tr>
<tr><td>Drew</td><td>3300</td></tr>
<tr><td>Earl</td><td>4000</td></tr>
</table>
</div>
<div class="section">
<H2>For out sample race:</H2>
<ul>
<li>Cut off = (3000+3100+3200+3300+4000)*1.05/5 = 3320</li>
<li>Average of all results bellow the cut off is = (3000+3100+3200+3300)/4 = 3150 </li>
<li>Audit = (competiors corrected time / Race Average) * 1000 rounded to the nearest whole number</li>
</ul>
</div>
<div class="section">
<table><tr><th>Competitor</th><th>Audit</th></tr>
<tr><td>Ade</td><td>3000/3150*1000 = 952</td></tr>
<tr><td>Bob</td><td>3100/3150*1000 = 984</td></tr>
<tr><td>Carl</td><td>3200/3150*1000 = 1016</td></tr>
<tr><td>Drew</td><td>3300/3150*1000 = 1048</td></tr>
<tr><td>Earl</td><td>4000/3150*1000 = 1269</td></tr>
</table>
</div>

<div class="section">
<p>For each competitor the average of all there Audits is taken to determine their personal number,  any audits greater than 1500 are not included in the average,  to discard particularly bad races where a competitor has lost a lap due to being OCS  or capsized a lot!</p>
<p>To use the personal handicap the formular is:</p>
<p>Personal correct time = PY corrected time / Personal handicap * 1000</p>
<p>Current personal handcap list as of: '''

html += str(datetime.date.today())

html += '''</p>
note a personal number of 0 doesn't mean your infinately fast (it just means we don't have enough data yet)
</div>
'''
html += '<div><table class="sortable"><thead><tr><th>QE</th><th>Sailor</th><th>Class</th><th>Personal Handicap</th><th>No Races</th></tr></thead><tbody>\n'
csv = ""

for qe in QES:
    newPersonal = 0
    if len(qe[2]) > 0:
        for e in qe[2]:
            if e < 1500:
                newPersonal += e
            else:
                newPersonal += 1500
        newPersonal = int(newPersonal / len(qe[2]))
    if newPersonal == 0:
        newPersonal = qe[1]
    #print(qe[0], newPersonal, len(qe[2]))
    personalHTMLString = str(newPersonal)
    if newPersonal == 0: personalHTMLString = "No Data 0"
    html += "<tr><td>" + qe[0] + "</td><td>"  + qe[3][QEcols['HELM']]+"<br>"+qe[3][QEcols['CREW']] + "</td><td>" \
    + qe[3][QEcols['CLASS']] + "</td><td>" + personalHTMLString \
    + "</td><td>" + str(len(qe[2])) + "</td></tr>\n"
    csv += qe[0] + "," + qe[3][1] + "," + qe[3][2] + "," + qe[3][3] + "," + qe[3][4] +\
           "," + str(newPersonal) + "," + qe[3][6] + "," + qe[3][7] +"\n"

html += '</tbody></table></div></body><script src="../js/sortable.js"></script></html>\n'

open("audit.csv","w").write(csv)
open("html/personalHandicaps.html", "w").write(html)
