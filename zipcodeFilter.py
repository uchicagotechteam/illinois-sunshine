import csvkit

def main():
	zip_data = open('./tmp/zipcode/zipcode.csv', 'r')
	ILZip = open('./tmp/ILZip.csv', 'w')
	csvwriter = csvkit.py2.CSVKitWriter(ILZip)
	zipread = csvkit.py2.CSVKitReader(zip_data)
	
	count = 0
	for z in zipread:
		if count == 0:
			csvwriter.writerow(z)
			count += 1
		
		if len(z) > 0 and z[2] == 'IL':
			csvwriter.writerow(z)
	ILZip.close()
	
if __name__ == '__main__':
	main()