# Box Score Search Scraper
# Team box search: http://stats.nba.com/search/team-game/#
# Player box search: http://stats.nba.com/search/player-game/#

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import csv
import time
import sys


# This function converts an html file with a table and returns two lists:
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

def pull_up_the_data(driver): 
	
	ex_button = driver.find_element_by_class_name("close")
	ex_button.click()

	team_selector = driver.find_element_by_xpath('//*[@id="streak-finder"]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[3]/div/div[4]')
	team_selector.click()
	pistons_button = driver.find_element_by_xpath('//*[@id="streak-finder"]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[2]/ul/li[11]')
	pistons_button.click()


	season_from_button = driver.find_element_by_xpath('//*[@id="streak-finder"]/div[2]/section/div/div[3]/div/div/form/div/section[1]/div/div[5]/div/input')
	season_from_button.click()
	season_from_button.send_keys('09/01/2010')
	run_button = driver.find_element_by_class_name("run-it")
	run_button.click()

	while True:
		try:
			driver.implicitly_wait(1)
			load_more_button = driver.find_element_by_xpath('//*[@id="stat-table"]/nba-stat-table/div[2]/div/a')
			load_more_button.click()

		except:
			break

	return;
	
def find_table(driver):
	table = driver.find_element_by_xpath('//*[@id="stat-table"]/nba-stat-table/div[1]')
	if table:
		return table
	else:
		return False

try:	
	WEBSITE = sys.argv[1]
	FILE_OUT = sys.argv[2]	
except ValueError:
	print "Wrong arguments passed. Function needs two arguments- \'python scraper.py [link] [output file]\'"
	

# Selenium is used to automate web browser clicks and find the HTML for data table on page

driver = webdriver.Chrome('./chromedriver')
driver.get(WEBSITE)
pull_up_the_data(driver)
table = WebDriverWait(driver, 10).until(find_table)	# wait until table found if needed
html = table.get_attribute('innerHTML')
headers, rows = get_data(html) 
write_table_to_file(FILE_OUT, headers, rows)

driver.quit()
print "Data from " + WEBSITE + " written to " + FILE_OUT