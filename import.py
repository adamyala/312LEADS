import inspect, os
import sqlite3
import requests
import json
from pygeocoder import Geocoder

import csv
def csv_to_list(file_path):
	datafile = open(file_path, 'r')
	datareader = csv.reader(datafile)
	data = []
	for row in datareader:
		data.append(row)
	return data

main_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#json method
# r = requests.get('http://data.cityofchicago.org/resource/4ijn-s7e5.json')
# violations = r.json()

#csv method
violations = csv_to_list(main_dir + '/Food_Inspections.csv')  

with sqlite3.connect(main_dir + '/abcproject.db') as connection:

	c = connection.cursor()

#i want business and zip and license and address
	#loop through businesses and get a list
	#make dict
#loop through list and make array of each business's comments if comment fits in code

	c.execute("DROP TABLE business")
	c.execute("DROP TABLE violations")

	c.execute("CREATE TABLE business(name TEXT, license TEXT, address TEXT, zipcode TEXT)")
	c.execute("CREATE TABLE violations(license TEXT, comment TEXT, violationnum TEXT)")

	headers = True
	for violation in violations:
		# print violation
		if headers:
			headers = False
		else:
			# print violation
#json method
		# try:
		# 	zipcode = violation['zip']
		# except:
		# 	zipcode = Geocoder.geocode(violation['address'] + 'CHICAGO IL')[0].postal_code

		# try:
		# 	facility = violation['facility_type']
		# except:
		# 	facility = ""

		# c.execute("""INSERT INTO business VALUES(?,?,?,?,?)""", (violation['dba_name'],violation['license_'],violation['address'] + 'CHICAGO IL', zipcode, facility))

#csv method
			address = violation[2] + 'CHICAGO IL'
			try:
				zipcode = violation[5]
			except:
				zipcode = Geocoder.geocode('CHICAGO IL')[0].postal_code
			name = violation[0]
			license = violation[1]
			c.execute("""INSERT INTO business VALUES(?,?,?,?)""",(name,license,address,zipcode))

			# print name
			# print license
			# print address
			# print zipcode

			try:
#json method
			# comments = violation['violations'].rsplit('|')
#csv method
				# print license[6]
				comments = violation[6].rsplit('|')

				# print comments

				for line in comments:
#json method
				# c.execute("""INSERT INTO violations VALUES(?,?,?,?)""", (violation['license_'], violation['inspection_date'][0:violations[0]['inspection_date'].find('T')], line[line.find('Comments:')+9:].strip(), line.strip()[0:2].rstrip('.')))
#csv method
					comment = line[line.find('Comments:')+9:].strip().rstrip()
					# print comment
					violationcode = line.strip()[0:2].rstrip('.')
					c.execute("""INSERT INTO violations VALUES(?,?,?)""", (license, comment,violationcode ))
			except:
				pass

print 'ran with no errors'