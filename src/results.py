#!/usr/bin/env python3
import os
import json
from serise import Series
from collections import namedtuple
from index import index

seriesDetails = namedtuple('SeriesDetails', ['name', 'pyFile', 'QEFile'])
pyFile,QEfile = json.loads(open("config.json","r").read())

s = seriesDetails("NewYearsDay","2025.txt","2026_QE_JAN.txt")
Series(s.pyFile,s.QEFile,{s.name.lower()},s.name,toCount=1).filterByBoatType("M").summary(False,False, f"html/{s.name}Monos.html")
Series(s.pyFile,s.QEFile,{s.name.lower()},s.name,toCount=1).filterByBoatType("C").summary(False,False, f"html/{s.name}Cats.html")
Series(s.pyFile,s.QEFile,{s.name.lower()},s.name,toCount=1).summary(False, False, f"html/{s.name}.html")

normalScoredSeries = [seriesDetails("Icicle","2025.txt","2026_QE_JAN.txt"),seriesDetails("fastnet","2026.txt","2026_QE_APR.txt")]
cupSeries = [seriesDetails("Houghton","2026.txt","2026_QE_APR.txt")]
"""
					  seriesDetails("Fastnet","2025.txt","2025_QE_APR.txt"),
					  seriesDetails("Portland","2025.txt",None),
					  seriesDetails("Rockall","2025.txt", "2025_QE_SEP.txt"),
					  seriesDetails("Autumn","2025.txt","2025_QE_OCT.txt"),
					seriesDetails("chrisJanes","2025.txt","2025_QE_APR.txt")]
cupSeries = [seriesDetails("Caulcott","2025.txt","2025_QE_JUL.txt"),
					  seriesDetails("Watts","2025.txt","2025_QE_SEP.txt"),
					  seriesDetails("Blackaby","2025.txt","2025_QE_APR.txt")]
noScoreSeries = [seriesDetails("Wednesday","2025.txt","2025_QE_SEP.txt"),
                    seriesDetails("funDoubles","2025.txt","2025_QE_SEP.txt")]
allCountSeries = [seriesDetails("ShortCourse1","2025.txt","2025_QE_APR.txt"),
                    seriesDetails("ShortCourse2","2025.txt","2025_QE_APR.txt"),
                    seriesDetails("ShortCourse3","2025.txt","2025_QE_APR.txt"),
                    seriesDetails("ShortCourse4","2025.txt",None)]


Series("2025.txt","2025_QE_SEP.txt",{"fastnet","rockall"},"Mono Championship").filterByBoatType("M").summary(True, True, f"html/ChampionshipMonos.html")
Series("2025.txt","2025_QE_SEP.txt",{"fastnet","rockall"},"Cat Championship").filterByBoatType("C").summary(True, True, f"html/ChampionshipCats.html")
Series("2025.txt","2025_QE_SEP.txt",{"fastnet","rockall"},"Championship").summary(True, True, f"html/Championship.html")


for d in normalScoredSeries + noScoreSeries + allCountSeries + cupSeries:	
	if (d.name).lower() in os.listdir():
		continue
	else:
		os.mkdir(d.name.lower())
"""
for s in normalScoredSeries + cupSeries:
    if s.QEFile != None:
        Series(s.pyFile,s.QEFile,{s.name.lower()},s.name).filterByBoatType("M").summary(True, True, f"html/{s.name}Monos.html")
        Series(s.pyFile,s.QEFile,{s.name.lower()},s.name).filterByBoatType("C").summary(True, True, f"html/{s.name}Cats.html")
        Series(s.pyFile,s.QEFile,{s.name.lower()},s.name).summary(True, True, f"html/{s.name}.html")
"""
for s in noScoreSeries:
    if s.QEFile != None:
        Series(s.pyFile, s.QEFile, {s.name.lower()},s.name,toCount=0).summary(False,False, f"html/{s.name}.html")


for s in allCountSeries:
    if s.QEFile != None:
        print(s.name)
        Series(pyFile, s.QEFile,{s.name.lower()},s.name,countAll=True).summary(True, True, f"html/{s.name}.html")

BoatTypes = ["Singles","Lasers","Cats","Doubles"]
for type in BoatTypes:
    Series("2025.txt", "2025_QE_APR.txt",  {"fastnet","rockall"},type).filterByBoatType(type[0]).summary(True,False,f"html/{type}.html")

AgeGroups = ["Seniors","Masters","Grandmasters"]
for type in AgeGroups:
    Series("2025.txt", "2025_QE_APR.txt",  {"fastnet","rockall"},type).filterByAge(type[0]).summary(True,False,f"html/{type}.html")
"""
index({"General Series" : [s.name for s in normalScoredSeries]})
"""
	"Championship" :["Championship"],
       "Cup Series" : [s.name for s in cupSeries],
       "Informal Series" : [s.name for s in noScoreSeries],
       "Short Course" : [s.name for s in allCountSeries],
       "Age Groups Series" : AgeGroups,
       "Boat Type Series" : BoatTypes
})

"""
