import os

class index:
    def __init__(self,seriesLists):
        year = "2026"
        links = ""
        for seriesDict in seriesLists:
            links += '''<div class="overflow-auto">
                    <div class="carousel-container">'''
            for s in seriesLists[seriesDict]:
                print(s)
                image = "default.jpg"
                for ext in [".jpg",".png"]:
                    if s+ext in os.listdir("/var/www/html/images"):
                        image = s + ext
                if s+".html" in os.listdir("html"):
                    links +=f'''<a href="{s}.html" class="carousel-item" style="background-image: url(/images/{image})">
                                    <div class="overlay gradient"></div>
                                    <div class="carousel-text"><h3>{s} Series</h3></div>
                                    <div class="flex-inline"><div class="carousel-item-label">{seriesDict}</div></div>
                                </a>'''
            links += "</div></div>"                    
        links += '''<div class="overflow-auto">
                    <div class="carousel-container">'''
        links += '''<a href="pursuit.html" class="carousel-item" style="background-image: url(/images/default.jpg)">
                                    <div class="overlay gradient"></div>
                                    <div class="carousel-text"><h3>Pursuit Series</h3></div>
                                    <div class="flex-inline"><div class="carousel-item-label">pursuit</div></div>
                                </a>'''
        links += "</div></div>"

        template = f'''<html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>SWSC Sailing Results</title>
            <link rel="icon" type="image/x-icon" href="/../images/favicon.png">
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0, minimal-ui">
            <link rel="stylesheet" href="../styles.css">
            <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
            <meta name="description" content="Check out the sailing results at Stewartby Water Sports Club: series standings, race results, and personal handicaps.">

            <!-- Open Graph meta tags for sharing -->
        <meta property="og:title" content="SWSC Sailing Results" />
        <meta property="og:description" content="Check out the sailing results at Stewartby Water Sports Club: series standings, race results, and personal handicaps." />
        <meta property="og:image" content="https://results.swsc.org.uk/images/IcicleSeries2025OG.png" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:url" content="https://results.swsc.org.uk/index.html" />
        <meta property="og:type" content="website" />
        </head>

        <body>
            <header class="section">
                <div class="container ">
                    <div class="group align-centre">
                    <div class="horizontal-wrapper">	
                    </div>
                    <a class="on-surface" href="../index.html">Results</a>
                    <h1 class="display-small on-surface">{year}</h1>
                </div>
            </header>
            <div class="divider"></div>
                <div class="section">
                    <div class="container">
                        <div class="layout-1-column">
                            <div class="padding overflow-auto">
                                {links}
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>'''
        open("html/index.html","w").write(template)
