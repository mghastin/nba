# Reference: Thanks to @royh21k on github for his helpful tutorial at 
# https://nycdatascience.com/blog/student-works/web-scraping/web-scraping-nba-stats/

# NBA Team Stats Website: http://stats.nba.com/team/1610612765/traditional/ 
# link above is for pistons

from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

def get_data(html):
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find("table")
	headers = [header.text.encode('utf8')  for header in table.find_all("th")]
	rows = []
	for row in table.tbody.find_all("tr"):
		cells = [cell.text.encode('utf8')  for cell in row.find_all("td")]
		rows.append(cells)
	return headers, rows;
	
def write_table_to_file(filename, headers, rows):
	with open(filename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(rows)
	f.close()
	return;

driver = webdriver.Chrome('./chromedriver')
driver.get('http://stats.nba.com/team/1610612765/traditional/')
time.sleep(5)

tables = driver.find_elements_by_tag_name('nba-stat-table') 	# get data table from page
html_list = [table.get_attribute('innerHTML') for table in tables]
data = []
headers = []
for html in html_list:
	headers, rows = get_data(html)
	data += rows #concat the tables
write_table_to_file('team_data.csv', headers, data)
	

print "Team data for current season from stats.nba.com written to team_data.csv"

