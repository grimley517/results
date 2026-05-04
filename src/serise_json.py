import math
import os
import datetime
import copy
from race import Race
from entry import Entry
from QE import QE
from helm import Helm
from seriesEntry import SeriesEntry

class Series:
    def __init__(self, handicapsFile, QEfile, racesDirs, name, toCount=None, countAll=False):
        self.toCount = toCount
        self.countAll = countAll
        self.name = name
        self.races = []
        self.PYs = dict()
        self.types = dict()
        PYcols = {'CLASS': 0, 'PY': 1, 'TYPE': 2, 'RIG': 3, 'CREW': 4, 'KITE': 5}
        for line in open(handicapsFile, "r").readlines():
            tokens = line.split(",")
            if tokens[0] != "":
                self.PYs[tokens[PYcols['CLASS']]] = int(tokens[PYcols['PY']])
                self.types[tokens[PYcols['CLASS']]] = tokens[PYcols['TYPE']]
        
        # Parse QE file and build list of QE objects
        self.QEs = []
        ln = 0
        for line in open(QEfile, "r").readlines():
            ln += 1
            qe = QE(line, self.PYs)
            if qe.dinghy in self.types.keys():
                qe.type = self.types[qe.dinghy]
                self.QEs.append(qe)
            elif len(line.strip()) > 0:
                print(f"dinghy type not in handicaps file on LineNo: {ln}: {line}")
        
        # Read race files
        files = []		
        for racesDir in racesDirs:
            dirlist = os.listdir(racesDir)			
            for f in dirlist:
                if f.endswith(".race"):  
                    files.append(os.path.join(racesDir, f))
				
        # Sort files by race number, AM/PM, and date
        files.sort(key=lambda x: int(x.split(" ")[1]), reverse=False)  # race No
        files.sort(key=lambda x: x.split(" ")[0].upper(), reverse=False)  # AM/PM			
        files.sort(key=lambda x: int(datetime.datetime.strptime(x.split(" ")[2], "%d-%m-%Y.race").timestamp()), reverse=False)  

        # Add races to the series
        for x in files:
            if x.endswith(".race"):
                r = Race([], self.QEs)
                r.load(x)
                self.races.append(r)

    def filterByBoatType(self, f):
        for r in self.races:
            newEntriesList = []
            for e in r.entries:
                if e.QE.type == f:
                    newEntriesList.append(e)
                if f == "M" and e.QE.type != "C":
                    newEntriesList.append(e)
            r.entries = newEntriesList
        return self

    def filterByAge(self, f):
        for r in self.races:
            newEntriesList = []
            for e in r.entries:
                if e.QE.ageGroup == f:
                    newEntriesList.append(e)
            r.entries = newEntriesList
        return self

    def generateJSONResults(self, score=True, personal=True):
        """
        Generates a dictionary with three keys:
          - seriesResults: overall series standings based on PY results
          - personalSeriesResults: overall standings based on personal results
          - individualRaces: list of individual race results
        """
        entries = {}
        # Build a dictionary of competitors using their helm name
        for r in self.races:
            for e in r.entries:
                helm = e.QE.helm
                if helm in entries:
                    if e.QE.dinghy not in entries[helm]["boats"]:
                        entries[helm]["boats"].append(e.QE.dinghy)
                else:
                    entries[helm] = {
                        "boats": [e.QE.dinghy],
                        "resultsPY": [],
                        "resultsPersonal": []
                    }
        # Set a default "did not count" (dnc) value
        dnc = len(entries) + 1
        for r in self.races:
            r.score(dnc)
        # Collect results for each race
        for r in self.races:
            for helm in entries.keys():
                result = dnc
                resultPersonal = dnc
                for e in r.entries:
                    if e.QE.helm == helm:
                        result = e.PYplace
                        resultPersonal = e.personalPlace
                entries[helm]["resultsPY"].append(result)
                entries[helm]["resultsPersonal"].append(resultPersonal)
        
        # Determine how many races count
        if self.toCount is None:
            toCount = int(math.ceil(len(self.races) / 3) + 1)
            if toCount > len(self.races):
                toCount = len(self.races)
        else:
            toCount = self.toCount
        if self.countAll:
            toCount = len(self.races)
        
        # Calculate overall scores (simple sum over counted races)
        for helm, data in entries.items():
            valid_results = data["resultsPY"][:toCount]
            data["overallScorePY"] = sum(valid_results) if valid_results else None
            valid_personal = data["resultsPersonal"][:toCount]
            data["overallScorePersonal"] = sum(valid_personal) if valid_personal else None

        # Prepare individual race data
        individualRaces = []
        for r in self.races:
            race_info = {
                "raceFile": os.path.basename(r.f),
                "PYResult": r.PYresult(),         # You may want to structure this further
                "personalResult": r.personalResult()  # Ditto
            }
            individualRaces.append(race_info)
        
        # Return the complete JSON structure
        return {
            "seriesResults": entries,
            "personalSeriesResults": entries,  # Same data; can be separated if desired
            "individualRaces": individualRaces
        }
