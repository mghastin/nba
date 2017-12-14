from subprocess import Popen, PIPE
import sqlite3
import pandas

# read csv files into a data frame, then write to sqlite database table

def get_csv_files():
	# get all the csv filenames stored in data folder
	print "I'm getting all the data files"
	p = Popen(["ls", "-Rx", "data"], stdout=PIPE, stderr=PIPE)
	output = p.communicate()[0]
	full_list = output.split()
	file_list = [string for string in full_list if ".csv" in string] # take out anything that isn't a csv file
	return file_list;

# open up database connection
print "connecting to database"
conn = sqlite3.connect('nba.db')

for file in get_csv_files():
	file_with_path = "data/" + file
	print "I'm going to read " + file_with_path
	df = pandas.read_csv(file_with_path, encoding = 'utf8')
	table_name = file.replace('.csv', '')
	print "Table name in database will be: " + table_name
	print "I'm going to send to sql!"
	df.to_sql(table_name.decode('utf-8'), conn, if_exists='replace', index=False)

conn.close()
