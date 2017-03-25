#!/usr/bin/python

import sys
import requests
import csv
from bs4 import BeautifulSoup
import subprocess

base_url = 'http://www.nasdaq.com/symbol/'
tickers = [] # This will hold the ticker symbols

if(len(sys.argv) > 2):
	print "Too many arguments provided."
else:
	# Open the filename provided and read in all the ticker symbols
	with open(sys.argv[1]) as f:
		for line in f:
			if line.rstrip():
				tickers.append(line.strip('\n'))
		# Iterate through the tickers array and pull historical data from NASDAQ
		for i in tickers:
			url = base_url + i + "/historical"
			out_csv = i+".csv"
			page = requests.get(url).text
			soup = BeautifulSoup(page, 'lxml')
			tableDiv = soup.find_all('div', id="historicalContainer")
			tableRows = tableDiv[0].findAll('tr')
			historical_data = []
			# This loop will actually retrieve the information
			for tableRow in tableRows[2:]:	
				row = list(tableRow.getText().split())
				# The first entry is the date. Turn into a string
				row[0] = str(row[0])
				# The last entry is the volume. Turn into int.
				row[len(row)-1] = int(row[len(row)-1].replace(',',''))
				# Every other entry is a price of the stock so convert to float
				for i in range(1, len(row)-1):
					row[i] = float(row[i])
				# Historical data is now a lists of lists for every day prices
				historical_data.append(row)

			# Create a csv file with the name of the ticker symbols. Add headers and then write in the historical data.
			with open(out_csv, 'wb') as csvFile:
					writer = csv.DictWriter(csvFile, fieldnames = ["Date", "Open", "High", "Low", "Close/Last", "Volume"])
					writer.writeheader()
					wr = csv.writer(csvFile, delimiter=",", quoting=csv.QUOTE_NONE)
					wr.writerows(historical_data)


subprocess.call("./copycsv.sh")
				
				


		
	

