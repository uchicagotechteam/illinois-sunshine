import matplotlib
import pandas as pd
import numpy as np
import json
import csv
from Queue import Queue
from threading import Thread
import requests
import csvkit
import datetime


#Zipcodes given by http://www.boutell.com/zipcodes/
url = "http://illinoissunshine.org/api/"

def main():
	
	#Request Committee data into JSON 
	respC = requests.get(url + 'committees/') #response object that holds committees
	coms = respC.json()['objects'] #List of committees
	
	#Open files to read committee and receipts data into
	#com_data = open('./tmp/CommitteeData.csv', 'w')
	#csvwriter = csvkit.py2.CSVKitWriter(com_data)
	
	#Load zipcodes into a csv file
	zip = open('./tmp/ILZip.csv', 'r')
	zipread = csvkit.py2.CSVKitReader(zip)
	zipList = []
	for z in zipread:
		zipList.append(z)
		
	#Loop through committees
	count = 0
	for c in coms:
	
		#Find the lat/long for cth committee's zipcode
		found = False
		for z in zipList:
			comzip = c['zipcode'][0:5]
			if len(z) > 0 and comzip == z[0]:
				c['lat'] = z[3]
				c['lon'] = z[4]
				found = True
				break
		
		if found == False:
			c['lat'] = 0
			c['lon'] = 0
		
		#Aggregate receipts for all years for cth committee
		#NEED TO CHANGE 2015 TO 1994
		#Instead of calling by year, simply get all receipts for each committee
		#and sort that way
		# for yr in range(2014, 2016):
			# create_date = c['creation_date']
			# cyr = datetime.datetime.strptime(create_date, '%Y-%m-%dT%H:%M:%S').year
			# if yr >= cyr:
				# receipt_dict = agg_receipts(c['id'], yr)
				# c[str(yr) + '_receipt_volume'] = receipt_dict['receipt_volume']
				# c[str(yr) + '_receipt_counter'] = receipt_dict['receipt_counter']
			# else:
				# c[str(yr) + '_receipt_volume'] = 0
				# c[str(yr) + '_receipt_counter'] = 0
		
		for yr in range(1994, 2017):
			c['receiptVolume' + str(yr)] = 0
			c['receiptCounter' + str(yr)] = 0
			
		resp_rec = requests.get(url + 'receipts/?committee_id=' + str(c['id']))
		
		if resp_rec.json()['meta']['total_rows'] != 0:
			receipts = resp_rec.json()['objects'][0]['receipts']
			#print(len(receipts))
			for r in receipts:
				received_yr = datetime.datetime.strptime(r['received_date'], '%Y-%m-%dT%H:%M:%S').year
				amt = r['amount']
				c['receiptVolume' + str(received_yr)] += amt
				c['receiptCounter' + str(received_yr)] += 1
			
			
		#Write data to csv file
		#if count == 0:
		#	header = c.keys()
		#	csvwriter.writerow(header)
		#	count += 1
		#csvwriter.writerow(c.values())
	geojson = { "type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", 'coordinates': [c['lon'], c['lat']]},"properties": c } for c in coms]}
	
	#print geojson
	with open('./tmp/com_data.json', 'w') as outfile:	
		outfile.write(json.dumps(coms))
	
	with open('./tmp/geojson_com_data.json', 'w') as outfile:
		outfile.write(json.dumps(geojson))

# def agg_receipts(cid, yr):
	# resp_rec = requests.get(url + 'receipts/?committee_id=' + str(cid) + '&received_date__lt=' + str(yr+1)
			# + '-01-01T00:00:00&received_date__ge=' + str(yr) + '-01-01T00:00:00') #Get receipts for the cid committee within the year yr
	
	# #Store volume and counter within dict
	# dict = {}
	# if(resp_rec.json()['meta']['total_rows'] == 0):
		# dict['receipt_volume'] = 0
		# dict['receipt_counter'] = 0
		# return dict
	
	# com_rec = resp_rec.json()['objects'][0]['receipts'] #0 gives us the committee {only object in objects list}
	
	# #Loop through receipts to calculate volume and counter
	# receipt_volume = 0
	# receipt_counter = 0
	# for i in range(0, len(com_rec)):
		# receipt_volume += (com_rec[i]['amount'])
		# receipt_counter += 1
	# dict['receipt_volume'] = receipt_volume
	# dict['receipt_counter'] = receipt_counter
	# return dict
	
if __name__ == '__main__':
	main()