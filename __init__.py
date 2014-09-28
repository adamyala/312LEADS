import requests
import sqlite3
import inspect, os

from flask import Flask, render_template, request, g
from flask.ext.mail import Mail, Message
from pygeocoder import Geocoder

app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.sendgrid.net',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'azure_c49eb65c111aa3e4526967bdbd38af9d@azure.com',
    MAIL_PASSWORD = 'lT12x6P86P3GzsN',
))

mail = Mail(app)

import csv
def csv_to_list(file_path):
	datafile = open(file_path, 'r')
	datareader = csv.reader(datafile)
	data = []
	for row in datareader:
		data.append(row)
	return data

app.database = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/abcproject.db'
def connect_to_database():
	return sqlite3.connect(app.database)

@app.route("/")
def main():
	return render_template('index.html')

import ast
@app.route('/email_dump/<leads>', methods=['GET', 'POST'])
@app.route('/email_dump/', defaults={'leads': None}, methods=['GET', 'POST'])
def email_dump(leads):

	jobdict = {
		'Food Wholesaler': '1',
		'Restaurant Supply Company': ['1', '2', '4', '6'],
		'HVAC Company/Refrigeration Supply': ['2', '3'],
		'Pharmacy': '5',
		'Construction Company': ['11', '26', '34', '35', '36', '37', '38'],
		'Electrician': ['2', '17', '22', '36'],
		'Staffing Agency': ['21', '23', '27', '31', '33', '41', '42', '44', '70'],
		'Appliance Repair Company': ['2', '3'],
		'Property Management Company': ['19'],
		'Waste Management Company': ['19','20'],
		'Pest Control Company': ['18','23'],
		'Plumbing Company': ['7', '9', '10', '11', '12', '22', '24', '26', '27', '38']
	}

	if request.method == 'POST':
		subject = {}
		for field in request.form:
			subject[field] = request.form[field]
	g.db = connect_to_database()

	main_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

	# licenses = csv_to_list(main_dir + '/Licenses.csv')

	# violations = csv_to_list(main_dir + '/Food_Inspections.csv')

	# result = []

	# codelist = jobdict[subject['occupation']]

	# bizlist = []
	# i = 0
	# while len(bizlist) < 10:
	# 	if licenses[i][1] == subject['zipcode']:
	# 		bizlist = bizlist.append(licenses[i])

	# loop through unique license list
		# only take businesses that match zip
		# stop at 10

	result = []
	# for biz in bizlist:
	# 	print 'biz is' + biz
	# 	for violation in violations:
	# 		print violation + 'for ' + biz
	# 		if biz[0] == violation[1] and biz[1] == violation[5]:
	# 			comments = violation[6].rsplit('|')
	# 			bizcomments = []
	# 			for comment in comments:
	# 				if comment.strip()[0:2].rstrip('.') in jobdict:
	# 					print 'writing comment'
	# 					bizcomments = bizcomments.append(comment[comment.find('Comments:')+9:].strip())
	# 	result = result.append([biz[3]+" - "+biz[2],bizcomments])

	# print result

	# load ordered list
		# loop through rows, take comments that match jobdict


	# for row in violations:

	# 	if violation[9] == "":
	# 		zipcode = Geocoder.geocode(violation[6] + 'CHICAGO IL')[0].postal_code
	# 	else:
	# 		zipcode = violation[9]

	# 	business = [
	# 		violation[0],
	# 		violation[3],
	# 		violation[6] + 'CHICAGO IL',
	# 		zipcode, violation[4]
	# 	]

	# 	comments = violation[13].rsplit('|')
	# 	# [
	# 	# 	violation[3],
	# 	# 	violation[10][0:violations[0][10].find('T')],
	# 	# 	line[line.find('Comments:')+9:].strip(),
	# 	# 	line.strip()[0:2].rstrip('.'))
	# 	# ]

	# 	if violations[9] == subject['zipcode'] and violations[3] in codelist:
	# 		result = result.apprend(violations[1] + ' - ' + violations[6] + ' CHICAGO IL')



	i = (subject['zipcode'].encode('ascii','ignore'),)
	print i
	tempbusinesses = g.db.execute("SELECT * FROM business WHERE zipcode='60609'")#?", i)
	businesses = tempbusinesses.fetchall()
	print businesses

	# violations = []
	j = jobdict[subject['occupation']]
	for code in j:
		violations = g.db.execute("SELECT * FROM violations WHERE violationnum=?", [code]).fetchall()
		for row in violations:
			row = list(row)
			for vio in row:
				vio = vio.encode('ascii','ignore')

	result = []
	businesses = [list(row) for row in businesses]
	for biz in businesses:
		result.append(biz[0]+" - "+biz[2]+biz[3])
		for vio in violations:
			temp = vio[0]
			if biz[1] == temp:
				result.append("  - "+vio[2])

	emailmess = """
			<table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
				<tr>
					<td bgcolor="#DF6060" style="padding: 15px 15px 15px 15px;">
					</td>
				</tr>
				<tr>
					<td bgcolor="#333" style="text-align:center; color:white">
						<h1><strong>312</strong>LEADS</h1>
					</td>
				</tr>
				<tr>
					<td bgcolor="#333" style="color:white; text-align:left; padding-left: 5%; padding-right: 5%; padding-bottom: 2%">"""

	for row in result:
		emailmess = emailmess + """<p style="color:white">""" + row + "</p>"

	emailmess = emailmess + """					</td>
				</tr>
				<tr>
					<td bgcolor="#333" style="text-align:center; color:#999; padding: 15px 15px 15px 15px;">
						Created at the MonkeyBars Open Build Hackathon
					</td>
				</tr>
			</table>
		"""

	msg = Message("Your Leads", sender="leads@312LEADS.com",
		html=emailmess,
		recipients=[subject['email']])
	msg.body = ''.join(result)
	mail.send(msg)

	return render_template('email_dump.html')

if __name__ == "__main__":
	app.debug = True
	app.run()
