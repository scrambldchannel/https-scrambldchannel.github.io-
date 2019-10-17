Title: Cricket Data Sources and Python
Date: 2019-09-28 16:24
Category: docs
Tags: cricket, python, data, api
slug: python-cricket-data
Authors: Alexander
Summary: Looking at ways to access cricket data using Python

Inspired by an enthralling Ashes series, I wanted to play around with cricket data available from various free and commercial sources out there.. Despite a bit of trawling, I couldn't really find a single document detailing what was available. 
 
## So what sources are there? 
 
I did a bit of Googling and also looked at what some of the obvious sites offered. Additionally, I looked for existing python libraries and played around with them. I was more interested in being able to crunch stats as opposed to creating widgets showing live scores, for example, but have looked at everything.
 
### Cricinfo
 
Every web literate person with even a passing interest in cricket will know Cricinfo. It's been owned by ESPN for years now and various old questions on Stack Exchange at Quora suggest they used to have an API for developers but that it was discontinued. That said, there are still some options for grabbing their data by leveraging feeds or scraping pages. 
 
#### RSS Feeds
 
This page lists the available RSS feeds. These can be parsed to get information on current matches and recent results.   
 
<http://www.espncricinfo.com/ci/content/rss/feeds_rss_cricket.html>
 
#### Python libraries
 
Searching on Github returns [quite a few results](https://github.com/search?l=Python&q=cricinfo&type=Repositories) but most are old and unloved. A couple stood out though (there are probably more of interest):
 
##### Cricpy
 
Provides a wealth of functions for scraping HTML pages as seems to be under active development. Has low-level functions that pull data and dump to CSV for local analysis as well as functions to create charts and perform statistical analysis. Seems geared towards people doing statistical analysis rather than creating apps. I definitely need to explore in more depth.
 
<https://github.com/tvganesh/cricpy>
 
##### python-espncricinfo
 
This is a simpler library that uses a combination of scraping as well as leveraging some (as far as I can tell) undocumented JSON files available on Cricinfo. It doesn't seem to be under active development though and some functions have bugs and some don't work at all. That said, it gave me an interesting insight into some data I didn't realise was easily accessible. 
 
<https://github.com/dwillis/python-espncricinfo>
 
 
### Cricbuzz
 
I'll confess to never really looking at Cricbuzz but it is another popular site dedicated to cricket news. There is a python library for accessing it.
 
#### pycricbuzz
 
I haven't really taken a look at this yet but it does seem to have been updated recently and have quite a few stargazers and forks.
 
<https://github.com/codophobia/pycricbuzz>
 
### Cricsheet

Cricsheet is an effort to create freely accessible ball-by-ball datasets for cricket matches. It took its inspiration from a project called Retrosheet, which attempts to do the same for MLB. It offers free to download and use data for a large subset of historical matches using YAML as well as a few other formats. It's an excellent resource for people wanting to churn through stats. 

<https://cricsheet.org/>


### Cricapi
 
This is a freemium API offering a free key that grants you 100 calls per day. It gives useful info about current matches and individual player stats but is probably more geared toward app developers than people just wanting to do analysis.
 
<https://www.cricapi.com/>
 
#### pycricapi
 
There is a library here that provides a basic wrapper for each endpoint.
 
<https://github.com/KarthikGangadhar/pycricapi>
 
### Rapid API
 
A few things turn up when searching Rapid API but I haven't really looked at them so far.
 
<https://rapidapi.com/search/cricket>
 
This seems to offer 2500 hits per day and a relatively cheap pricing model after that. Again it's geared toward app developers rather than statisticians. 
 
<https://rapidapi.com/dev132/api/cricket-live-scores/>
 
 
### Sportradar
 
Sportradar offers a number of different APIs for different sports. It's a premium service (ie quite expensive) but does provide some pretty useful stuff. I took advantage of their free trial and played around with a bit but I am limited to 1000 calls as part of the trial so haven't explored too much.
 
#### SportradarAPIs (python wrapper)
 
A wrapper already existed but didn't include a class to access the cricket endpoints so I added them. 
 
<https://github.com/johnwmillr/SportradarAPIs>
 
### Sportmonks
 
Sportmonks is another service providing APIs for all sorts of sports. They offer a free trial for 14 days but I haven't taken them up on this yet but might revisit this if I have a bit of time to make the most of it.
 
<https://www.sportmonks.com/cricket-api> - 14-day trial available
 
### Cricket API
 
I found this which is another premium service but without any option for a free trial that I could see. I've not looked at it beyond that.
 
<https://www.cricketapi.com/>