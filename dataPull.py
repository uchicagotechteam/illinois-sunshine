
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
			c[str(yr) + '_receipt_volume'] = 0
			c[str(yr) + '_receipt_counter'] = 0
			
		resp_rec = requests.get(url + 'receipts/?committee_id=' + str(c['id']))
		
		if resp_rec.json()['meta']['total_rows'] != 0:
			receipts = resp_rec.json()['objects'][0]['receipts']
			print(len(receipts))
			for r in receipts:
				received_yr = datetime.datetime.strptime(r['received_date'], '%Y-%m-%dT%H:%M:%S').year
				amt = r['amount']
				c[str(received_yr) + '_receipt_volume'] += amt
				c[str(received_yr) + '_receipt_counter'] += 1
			
			
		#Write data to csv file
		#if count == 0:
		#	header = c.keys()
		#	csvwriter.writerow(header)
		#	count += 1
		#csvwriter.writerow(c.values())
	with open('./tmp/com_data.json', 'w') as outfile:	
		json.dump(coms, outfile)

def agg_receipts(cid, yr):
	resp_rec = requests.get(url + 'receipts/?committee_id=' + str(cid) + '&received_date__lt=' + str(yr+1)
			+ '-01-01T00:00:00&received_date__ge=' + str(yr) + '-01-01T00:00:00') #Get receipts for the cid committee within the year yr
	
	#Store volume and counter within dict
	dict = {}
	if(resp_rec.json()['meta']['total_rows'] == 0):
		dict['receipt_volume'] = 0
		dict['receipt_counter'] = 0
		return dict
	
	com_rec = resp_rec.json()['objects'][0]['receipts'] #0 gives us the committee {only object in objects list}
	
	#Loop through receipts to calculate volume and counter
	receipt_volume = 0
	receipt_counter = 0
	for i in range(0, len(com_rec)):
		receipt_volume += (com_rec[i]['amount'])
		receipt_counter += 1
	dict['receipt_volume'] = receipt_volume
	dict['receipt_counter'] = receipt_counter
	return dict
	
	
	
	#comYear = [{} for x in range(1994, 2016)] #This is a list of dictionaries with the index of the list corresponding to the year (0 = 1994)
											  #So for the year 1994 (index = 0), there will be a dictionary which has keys of a committee id and 
											  #a value of dictionary holding receipt_volume, receipt_counter, and other stuff.
											  #So 1 entry in the list would look like [{committee_id1 : {receipt_volume : a, receipt_counter: b}, committee_id2 : {receipt_volume: x, receipt_counter: y}]
											  #I thought this would be easier to index by years if we were to implement the slider feature by year in the heat map. This may not be the best way to organize
											  #the data though.
	
	##The following block of commented code is an attempt to make the whole process of pulling data faster.
	##I was trying to implement running http requests simultaneously using a module called grequests (which I learned about on stackoverflow)
	##However the module seems to be outdated as it only is able to call google.com and bing.com. I may be trying to implement something
	##with FuturesSessions, but if you have any ideas on how to make multiple http requests simultaneously, please let me know.
	
	#List of committee ids
	# cids = [0 for x in range(0, len(coms))]
	# for j in range(0, len(coms)):
		# cids[j] = coms[j]['id']
		
	#Store urls to call in multiple instances
	# urls = []
	# for k in range(1994, 2016):
		# for j in range(len(cids)):
			# #Get urls for all cids for kth year
			# urls.append(url + 'receipts/?committee_id=' + str(cids[j]) + '&received_date__lt=' + str(k+1)
			# + '-01-01T00:00:00&received_date__ge=' + str(k) + '-01-01T00:00:00')
		
		# #Call request for all cids for kth year
		# rs = (grequests.get(u) for u in urls)
		# responses = grequests.map(rs)
		
		# #Calculate total receipts etc for each cid for kth year
		# for a in responses:
			# dict = {}
			# receipt_volume = 0
			# receipt_counter = 0
			# com_rec = a.json()['objects'][0]['receipts']
			# for i in range(0, len(com_rec)):
				# receipt_volume += com_rec[i]['amount']
				# receipt_counter += 1
			# dict['receipt_volume'] = receipt_volume
			# dict['receipt_counter'] = receipt_counter
			# comYear[k-1994][str(a.json()['objects'][0]['id'])] = dict
			# a.close()
		
		# #Clear urls for k+1 year
		# urls[:] = []
	
	
	#Loop through each committee
	#for j in range(0, len(coms)):
	#	cid = coms[j]['id']
		#Need to seperate by year
	#	for k in range(1994, 2016):
			#resp_rec = requests.get(url + 'receipts/?committee_id=' + str(cid) + '&received_date__lt=' + str(k+1)
			#+ '-01-01T00:00:00&received_date__ge=' + str(k) + '-01-01T00:00:00') #Get receipts for the jth committee within the kth year
			
	#		resp_rec = sess.get(url + 'receipts/?committee_id=' + str(cid) + '&received_date__lt=' + str(k+1)
	#		+ '-01-01T00:00:00&received_date__ge=' + str(k) + '-01-01T00:00:00')
			
			#If no receipts for this committee, then set receipt_counter and receipt_volunteer = 0
	#		if(resp_rec.json()['meta']['total_rows'] == 0):
	#			dict = {'receipt_volume': 0}
	#			dict['receipt_counter'] = 0
	#			continue
				
	#		com_rec = resp_rec.json()['objects'][0]['receipts'] #0 gives us the committee {only object in objects list}
			
	#		dict = {}
	#		receipt_volume = 0
	#		receipt_counter = 0
	#		for i in range(0, len(com_rec)):
	#			receipt_volume += (com_rec[i]['amount'])
	#			receipt_counter += 1
	#		dict['receipt_volume'] = receipt_volume
	#		dict['receipt_counter'] = receipt_counter
	#		comYear[k-1994][str(cid)] = dict
		
	#	print(comYear)
	
	#for i in range(1, len(respC.json()['objects'])):
	#	cid = respC.json()['objects'][i]['id']
	#	print(respC.json()['objects'][i]['id'])
	#	respR = requests.get(url + 'receipts/?committee_id=' + str(cid))
	#	print(respR)
	#	comId.append(cid)
	#	break
	#print(len(comId))
	#obj = json.loads(resp.json())
	#print()
	
	
	
if __name__ == '__main__':
	main()