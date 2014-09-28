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

print main_dir
r = requests.get('http://data.cityofchicago.org/resource/4ijn-s7e5.json')

violations = r.json()

# violations = csv_to_list(main_dir + '/Food_Inspections.csv')
# print violations

# print violations[0]

# with open("Output.txt", "w") as text_file:

with sqlite3.connect(main_dir + '/abcproject.db') as connection:
	c = connection.cursor()

	c.execute("CREATE TABLE business(name TEXT, license TEXT, address TEXT, zipcode TEXT, facility TEXT)")

	c.execute("CREATE TABLE violations(license TEXT, inspecdate TEXT, comment TEXT, violationnum TEXT)")

	for violation in violations:

		try:
			zipcode = violation['zip']
		except:
			zipcode = Geocoder.geocode(violation['address'] + 'CHICAGO IL')[0].postal_code

		# if violation[9] == "":
		# 	zipcode = Geocoder.geocode(violation[6] + 'CHICAGO IL')[0].postal_code
		# else:
		# 	zipcode = violation[9]

		try:
			facility = violation['facility_type']
		except:
			facility = ""

		# facility = violation[4]

		# text_file.write(violation['dba_name'] + " " + zipcode)
		# if zipcode == None: zipcode = ""
		# print violation[0]
		# print zipcode
		# text_file.write(violation[0] + ' ' + zipcode)

		# text_file.write('\n')

		# print violation['dba_name'] + " " + zipcode

		c.execute("""INSERT INTO business VALUES(?,?,?,?,?)""", (violation['dba_name'],violation['license_'],violation['address'] + 'CHICAGO IL', zipcode, facility))
		# c.execute("""INSERT INTO business VALUES(?,?,?,?,?)""", (violation[0],violation[3],violation[6] + 'CHICAGO IL', zipcode, facility))

		try:
			comments = violation['violations'].rsplit('|')
			# comments = violation[13].rsplit('|')

			for line in comments:
				c.execute("""INSERT INTO violations VALUES(?,?,?,?)""", (violation['license_'], violation['inspection_date'][0:violations[0]['inspection_date'].find('T')], line[line.find('Comments:')+9:].strip(), line.strip()[0:2].rstrip('.')))
				# c.execute("""INSERT INTO violations VALUES(?,?,?,?)""", (violation[3], violation[10][0:violations[0][10].find('T')], line[line.find('Comments:')+9:].strip(), line.strip()[0:2].rstrip('.')))
		except:
			pass

print 'ran with no errors'