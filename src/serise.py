import math
import os
import datetime
import copy
from race import Race
from entry import Entry
from QE import QE
from helm import Helm
from seriesEntry import SeriesEntry
import os



class Series:
	def __init__(self,handicapsFile,QEfile,racesDirs,name,toCount=None,countAll=False):
		self.toCount = toCount
		self.countAll = countAll
		self.name = name
		self.races = []
		self.PYs = dict()
		self.types = dict()
		PYcols = {'CLASS': 0, 'PY': 1, 'TYPE': 2, 'RIG': 3, 'CREW': 4, 'KITE': 5}
		for line in open(handicapsFile,"r").readlines():
			tokens = line.split(",")
			if tokens[0] != "":
				self.PYs[tokens[PYcols['CLASS']]] = int(tokens[PYcols['PY']])
				self.types[tokens[PYcols['CLASS']]] = tokens[PYcols['TYPE']]

		#parses and verify QES create a list of all helms with their QEs collated.
		self.QEs = []
		ln = 0
		for line in open(QEfile, "r").readlines():
			ln += 1
			qe = QE(line, self.PYs)
			if qe.dinghy in self.types.keys():
				qe.type = self.types[qe.dinghy]
				self.QEs.append(qe)
			elif(len(line.strip())>0):
				print(f"dinghy type not in handicaps file on LineNo: {ln}: {line}");			
			

		#read race files
		files = []		
		for racesDir in racesDirs:
			dirlist = os.listdir(racesDir)			
			for f in dirlist:
				if f[-5:] == ".race":  
					files.append(os.path.join(racesDir,f))
				
		#sort them
		files.sort(key=lambda x: int(x.split(" ")[1]), reverse=False)  #race No
		files.sort(key=lambda x: x.split(" ")[0].upper(), reverse=False)  #AM/PM			
		files.sort(key=lambda x: int(datetime.datetime.strptime(x.split(" ")[2],"%d-%m-%Y.race").timestamp()), reverse=False)  

		#add them to the series
		for x in files:
				print(x)
				if x[-5:] == ".race":
					r = Race([], self.QEs)
					r.load(x)
					self.races.append(r)


	def filterByBoatType(self,f):
		singles = []
		doubles = []
		cats = []
		lasers = []
		for r in self.races:
			newEntriesList = []
			for e in r.entries:
				if e.QE.type == f: newEntriesList.append(e)
				if f=="M" and e.QE.type != "C": newEntriesList.append(e)
			r.entries = newEntriesList
		return self


	def filterByAge(self,f):
		for r in self.races:
			newEntriesList = []
			for e in r.entries:
				if e.QE.ageGroup == f: newEntriesList.append(e)
			r.entries = newEntriesList
		return self

	def summary(self,silver,personal,outfile,score=True):	
		year = "2026"	
		headings =r"<tr><th>competitor(s)</th><th>Class(es)</th>"
		entries = dict()
		boats = []
		i = 1
		for r in self.races:
			headings += r"<th>" + str(i) + r"</th>"
			i += 1
			for e in r.entries:
				if e.QE.helm in entries.keys():
					if not(e.QE.dinghy in entries[e.QE.helm].boats):
						entries[e.QE.helm].boats.append(e.QE.dinghy)
				else:
					entries[e.QE.helm] = SeriesEntry(e.QE.dinghy,e.QE.helm)
				
		headings += r"<th>Score</th></tr>"
		#score all races with dnc value calculated
		dnc = len(entries) + 1
		for r in self.races:
			r.score(dnc)

		for r in self.races:
			for se in entries.keys():
				result = dnc
				resultpersonal = dnc
				for e in r.entries:
					if e.QE.helm == se:
						result = e.PYplace
						resultpersonal = e.personalPlace
						if e.QE.crew != "":
							entries[se].crews.add(f" {e.QE.crew} ({e.QE.dinghy})")
							#print("CREW: ",e.QE.crew)
				entries[se].resultsPY.append(result)
				entries[se].resultsPersonal.append(resultpersonal)
				
				#print(entries[se]scorePY ,entries[se].scorePersonal ,entries[se].name)

		with open(outfile, "w") as out:
			if self.toCount == None:
				toCount = int(math.ceil(len(self.races)/3) + 1)
				self.toCount = toCount
			toCountString = f"""There number of races scheduled races are as per the club callender 1/3 of the races +1 rounded up to the nearest whole number will be the number to count. Currently, {len(self.races)} races have been sailed, and {self.toCount} are counting toward competitors scores. Here are the latest standings"""
			buttons = ""
			if os.path.exists(f"html/{self.name}Cats.html") and os.path.exists(f"html/{self.name}Monos.html"):
				buttons = f'''<div class="segmented-button-wrapper"><a href="{self.name}.html" class="segmented-button first">Combined</a>
			<a href="{self.name}Monos.html" class="segmented-button">Monohulls</a>
			<a href="{self.name}Cats.html" class="segmented-button last">Catamarans</a></div>
		</div>'''
			if self.toCount == 0:
				toCount = self.toCount
				toCountString = "These races are informal so no series result is calcualted"
			
				if toCount > len(self.races): toCount = len(self.races)	
			else:
				toCount = self.toCount
			if self.countAll:
				toCount = len(self.races)
				toCountString = "In this serise all races count towards the result with no discards"
			print("ToCount:",toCount)
			#PY overall result
			out.write(f'''<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>{self.name} Series Results 2026</title>
		<link rel="icon" type="image/x-icon" href="../images/favicon.png">
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0, minimal-ui">
	<link rel="stylesheet" href="../styles.css">
	<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
	<meta name="description" content="Check out the {self.name} Series results at Stewartby Water Sports Club: series standings, race results, and personal handicaps.">

	 <!-- Open Graph meta tags for sharing -->
<meta property="og:title" content="{self.name} Series Results 2025" />
<meta property="og:description" content="Check out the {self.name} Series results at Stewartby Water Sports Club: series standings, race results, and personal handicaps." />
<meta property="og:image" content="https://results.swsc.org.uk/images/IcicleSeries2025OG.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:url" content="https://results.swsc.org.uk/2025/{self.name}.html" />
<meta property="og:type" content="website" />

</head>

<body>
	<div class="section">
		<div class="container ">
			<div class="group align-centre">
			<div class="horizontal-wrapper">	
			</div>
			<a class="on-surface" href="../index.html">Results > </a>
			<a class="on-surface" href="index.html">{year}</a>
			<h1 class="display-small on-surface">{self.name} Series Results</h1>
		
			<p class="body-medium max-width-70ch">{toCountString}</p>
		{buttons}
		
		</div>
	</div>
	<div class="divider"></div>
	<div class="section">
			<div class="container">
				<div class="layout-grid-2column">
					<div class="padding">
			<div class="group">
			<h2 class="headline-small">PY Results</h2>''')
#end header write	
		
#create summary

			if self.toCount != 0:
				summary = '''<p class="body-medium max-width-70ch">These results have been calculated using the Portsmouth Yardstick measurement, which allows you to compare your performance against other sailors in different boats. These results determine the overall winner of the series.</P>
				</div>
				<div class="overflow-auto surface-container-low border-radius-medium">'''
				summary += "<table>" + headings
				for se in entries.keys():
					entries[se].scoreSeries(toCount, dnc)
				entries = list(entries.values())
				entries.sort(key=lambda x: x.scorePY, reverse=False)
				for se in entries:summary += se.summary()
				summary += "</table>"
				#Personal overall result
				summary += '''</div>
				<div class="group">
				<h2 class="headline-small">Personal Results</h2>
				<p class="body-medium max-width-70ch">To win the personal handicap results, keep beating your own handicap more than anyone else! We use a rolling 12 months of race times, discarding unusually slow finishes, to find your personal handicap. Each time you sail faster, your handicap tightens up for the next race, and vice versa.</p>
				</div>
				<div class="overflow-auto surface-container-low border-radius-medium">'''
				summary += "<table>" + headings
				entries.sort(key=lambda x: x.scorePersonal, reverse=False)
				for se in entries:
					summary += se.summaryPersonal()
				summary += "</table>"
				summary += "</div></div>"
				out.write(summary)
			
			out.write('''<div class="padding">
<div class="group">
	<h2 class="headline-small">Individual Race Results</h2>
	<p class="body-medium max-width-70ch">These are the individual race results from each race in the series.</p>
</div>
<div class="reverse">''')
			for r in self.races:
				summary = ""
				pth, name = os.path.split(r.f)
				summary = f'''<details class="surface-container-low border-radius-extra-large">
				<summary>{name}</summary>
				<div class="overflow-auto">		
				{r.PYresult()}
				{r.personalResult()}
				</div>
				</details> '''
				out.write(summary)

				script ="""
				<script>
							// Close all other <details> when one is opened
	const allDetails = document.querySelectorAll('details');
	allDetails.forEach((detail) => {
	  detail.addEventListener('toggle', () => {
		if (detail.open) {
		  allDetails.forEach((otherDetail) => {
			if (otherDetail !== detail) {
			  otherDetail.open = false;
			}
		  });
		}
	  });
	});
  
	window.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname; // e.g. "/folder/IcicleMonos.html"
  document.querySelectorAll('a.segmented-button').forEach(link => {
    const linkFile = link.getAttribute('href'); // e.g. "IcicleMonos.html"
    if (currentPath.endsWith(linkFile)) {
      link.classList.add('current');
    }
  });
});
				</script>
				"""
				out.write(script)

			out.write("</body></html>")
		print("done")
