import sqlite3
import pandas

print "connecting to database"
conn = sqlite3.connect('nba.db')
QUERY = 'SELECT * FROM "pistons_player_box" \
		WHERE PLAYER = "Andre Drummond" OR \
	     	  PLAYER = "Reggie Jackson" OR \
	       	  PLAYER = "Tobias Harris" OR \
	       	  PLAYER = "Marcus Morris" OR \
	       	  PLAYER = "Stanley Johnson" OR \
	       	  PLAYER = "Ish Smith" OR \
	       	  PLAYER = "Kentavious Caldwell-Pope" OR \
	       	  PLAYER = "Avery Bradley";'  
print "Sending query"
pistons_df = pandas.read_sql_query(QUERY, conn, parse_dates = ["DATE"])
# Convert unicode numbers to numeric
columns_to_convert = ['FT%', 'FG%', '3P%']
for column in columns_to_convert:
	print "Currently converting row " + column
	num_rows, num_cols = pistons_df.shape
	for row in range(0, num_rows-1):
		pistons_df.at[pistons_df.index[row],column] = pandas.to_numeric( \
											pistons_df.at[pistons_df.index[row],column], \ 
											errors='coerce')



# Separate players + put in list, get data just for this season and last season

players = ['Andre Drummond', 'Reggie Jackson', 'Tobias Harris', 'Marcus Morris', \
			'Stanley Johnson', 'Ish Smith', 'Kentavious Caldwell-Pope', 'Avery Bradley']
player_data = {}

for player in players:
	QUERY = "(PLAYER == '" + player + "') & (DATE > '09/01/2016')"
	player_data[player] = pistons_df.query(QUERY)

# find season averages

#sum = 0
#sum += column
#for player in player_data
conn.close()

#>>> player_data['Andre Drummond'].query("DATE > '09/01/2017'").mean()
#player_data['Andre Drummond'].loc[:]["FT%"] = pandas.to_numeric(player_data['Andre Drummond'].loc[:]["FT%"], errors='coerce')