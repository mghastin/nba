# This module scrapes data from the NBA stats website and saves it to file
# python scraper.py [link] [output file]
# nba stats web address to be scraped is first argument
# second argument passed in the name of the output file (csv) you would like data to be
# saved to.

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

def find_table(driver):
	table = driver.find_element_by_tag_name('nba-stat-table')
	if table:
		return table
	else:
		return False


try:	
	WEBSITE = sys.argv[1]
	FILE_OUT = sys.argv[2]	
except ValueError:
	print "No arguments passed. Function needs two arguments- \'python scraper.py [link] [output file]\'"
	

# Selenium is used to automate web browser clicks and find the HTML for data table on page
# Website used a lot of js and clicking is needed to go through multiple pages

driver = webdriver.Chrome('./chromedriver')
driver.get(WEBSITE)

prev_table_html = ""
data = []
headers = []

while True:
	table = WebDriverWait(driver, 10).until(find_table)	# wait until table found if needed
	html = table.get_attribute('innerHTML')
	if html == prev_table_html:  # if not another page, stop and write data
		write_table_to_file(FILE_OUT, headers, data)
		break
	headers, rows = get_data(html) 
	data += rows # add the new table rows to data list
	prev_table_html = html
	try:
		next_page_button = driver.find_element_by_class_name("stats-table-pagination__next")
		next_page_button.click()
	except:
		write_table_to_file(FILE_OUT, headers, data)
		break

driver.quit()
print "Data from " + WEBSITE + " written to " + FILE_OUT


