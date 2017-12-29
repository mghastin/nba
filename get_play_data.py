from subprocess import call

plays = ["isolation", "transition", "ball-handler", "roll-man", "playtype-post-up",
			"spot-up", "hand-off", "cut", "off-screen", "putbacks", "playtype-misc"]

for play in plays:		
	print "http://stats.nba.com/players/" + play + "/"	
	call(["python", "scraper.py", "http://stats.nba.com/players/" + play + "/", 
			"data/" + play + ".csv"])
