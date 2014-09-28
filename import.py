import inspect, os
import sqlite3
import requests
import json
from pygeocoder import Geocoder

main_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

r = requests.get('http://data.cityofchicago.org/resource/4ijn-s7e5.json')

violations = r.json()

# print violations[0]

with sqlite3.connect(main_dir + '/abcproject.db') as connection:
	c = connection.cursor()

	c.execute("CREATE TABLE business(name TEXT, license TEXT, address TEXT, zipcode TEXT, facility TEXT)")

	c.execute("CREATE TABLE violations(license TEXT, inspecdate TEXT, comment TEXT, violationnum TEXT)")

	for violation in violations:

		try:
			zipcode = violation['zip']
		except:
			zipcode = Geocoder.geocode(violation['address'] + 'CHICAGO IL')[0].postal_code

		try:
			facility = violation['facility_type']
		except:
			facility = ""

		print zipcode

		c.execute("""INSERT INTO business VALUES(?,?,?,?,?)""", (violation['dba_name'],violation['license_'],violation['address'] + 'CHICAGO IL', zipcode, facility))

		try:
			comments = violation['violations'].rsplit('|')

			for line in comments:
				c.execute("""INSERT INTO violations VALUES(?,?,?,?)""", (violation['license_'], violation['inspection_date'][0:violations[0]['inspection_date'].find('T')], line[line.find('Comments:')+9:].strip(), line.strip()[0:2].rstrip('.')))
				
		except:
			pass

print 'ran with no errors'