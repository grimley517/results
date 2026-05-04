R1 = ["Richard Hargreves RS300",
"Tim Browning Streaker",
"Colin Wright Laser",
"Yossi Galliko Phantom"
"Dave Harrison Laser",
"Jim Strother Dzero",
"Gareth Farr A Class (Foiling)"]

R2 = ["Joel Walker LASER", "David Barr SOLO",
"Colin Clasper,Simon RS VISION",
"Tim Browning SPRINT 15"]

R3 = ["Mark Heij RS100","Dave Harrison LASER","Roger Folwer RS AERO 7"]

R4 = ["Joel Walker LASER","Tim Browning STREAKER","Yossi Galiko PHANTOM","Mark Heij Jamie Ratcliffe RS400","Eti Saltpeter PICO" ]

html = '<html><head><link rel="stylesheet" href="../styles.css"></head>\n'
for er,r in enumerate([R1,R2,R3,R4]):
	html += f"<h1>Pursuit {er+1}</h1>\n"	
	html += "<table><tr><th>Place</th><th>Competitor</th></tr>\n"
	for ec,c in enumerate(r):
		html += f"<tr><td>{ec+1}</td>><td>{c}</td></tr>\n"
	html += "</table>"
html += "</html>"

open("html/pursuit.html","w").write(html)
