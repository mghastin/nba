# Reference: Thanks to @royh21k on github for his helpful tutorial at 
# https://nycdatascience.com/blog/student-works/web-scraping/web-scraping-nba-stats/

# NBA Player Stats Website: http://stats.nba.com/players/advanced/?sort=TEAM_ABBREVIATION&dir=-1 
# (sorted by team)

# This module scrapes data from the NBA player stats website and saves it to file

from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time


# This function converts an html file, extracts the data table using the Beautiful Soup
# library, and returns two lists:
# 	1. header row
#	2. list of rows, each row a list of "cell" strings

def get_data(html):
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find("table")
	headers = [header.text.encode('utf8')  for header in table.find_all("th")]
	rows = []
	for row in table.tbody.find_all("tr"):
		cells = [cell.text.encode('utf8')  for cell in row.find_all("td")]
		rows.append(cells)
	return headers, rows;

# Write to csv file	

def write_table_to_file(filename, headers, rows):
	with open(filename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(rows)
	f.close()
	return;

# Selenium is used to automate web browser clicks and find the HTML for data table on page
# Website used a lot of js and clicking is needed to go through multiple pages

driver = webdriver.Chrome('./chromedriver')
driver.get('http://stats.nba.com/players/advanced/?sort=TEAM_ABBREVIATION&dir=-1')
time.sleep(5) # Give the page a chance to load

prev_table_html = ""
data = []
headers = []

while True:
	table = driver.find_element_by_tag_name('nba-stat-table') 	# get data table from page
	html = table.get_attribute('innerHTML')
	if html == prev_table_html:  # if not another page, stop and write data
		write_table_to_file('player_data.csv', headers, data)
		break
	headers, rows = get_data(html) 
	data += rows # add the new table rows to data list
	prev_table_html = html
	next_page_button = driver.find_element_by_class_name("stats-table-pagination__next")
	next_page_button.click()

driver.quit()
print "Player data for current season from stats.nba.com written to player_data.csv"


