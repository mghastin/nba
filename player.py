# player.py

import sqlite3
import pandas

class Player:
	
	def __init__(self, name):
		conn = sqlite3.connect('nba.db')
		QUERY = 'SELECT * FROM "pistons_player_box" \
		WHERE PLAYER = "' + name + '";'  
		self.df = pandas.read_sql_query(QUERY, conn, parse_dates = ["DATE"])
		# Convert unicode numbers to numeric, blank rows "-" go to NaN
		columns_to_convert = ['FT%', 'FG%', '3P%']
		for column in columns_to_convert:
			num_rows, num_cols = self.df.shape
			for row in range(0, num_rows):
				self.df.at[self.df.index[row],column] = pandas.to_numeric( \
													self.df.at[self.df.index[row],column], \
													errors='coerce')
		conn.close()
		self.name = name
		return;
	
	def average(self, season = '2017', attribute = None):
		# This function returns series with average for all stats if no specific attribute given
		DATE_QUERY = "DATE > '09/01/" + season + "' and DATE < '07/01/" + str(int(season)+1) + "'"
		if attribute:
			return self.df.query(DATE_QUERY).mean(attribute);
		else:
			return self.df.query(DATE_QUERY).mean();
			
	def median(self, season = '2017', attribute = None):
		DATE_QUERY = "DATE > '09/01/" + season + "' and DATE < '07/01/" + str(int(season)+1) + "'"
		if attribute:
			return self.df.query(DATE_QUERY).median(attribute);
		else:
			return self.df.query(DATE_QUERY).median();
			
	def mode(self, season = '2017', attribute = None):
		DATE_QUERY = "DATE > '09/01/" + season + "' and DATE < '07/01/" + str(int(season)+1) + "'"
		if attribute:
			return self.df.query(DATE_QUERY).mode(attribute, True);
		else:
			return self.df.query(DATE_QUERY).mode(0, True);
			
	def get_data(self, attribute, season = '2017'):
		DATE_QUERY = "DATE > '09/01/" + season + "' and DATE < '07/01/" + str(int(season)+1) + "'"
		return self.df.query(DATE_QUERY)[attribute];
		
	def get_attributes(self):
		return self.df.columns;
