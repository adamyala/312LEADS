import requests
import sqlite3
import inspect, os

from flask import Flask, render_template, request, g
from flask.ext.mail import Mail, Message
app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.sendgrid.net',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'azure_bedae6f1889ca6f6048eee57c8e6b6c2@azure.com',
    MAIL_PASSWORD = 'xjyV3jdU42InanO',
))

mail = Mail(app)

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
		'Food Wholesale': '1',
		'Restaurant Supplier': ['1', '2', '4', '6'],
		'HVAC/Refregiration': ['2', '3'],
		'Pharmacy': '5',
		'Construction': ['11', '26', '34', '35', '36', '37', '38'],
		'Electrician': ['2', '17', '22', '36'],
		'Staffing Agency': ['21', '23', '27', '31', '33', '41', '42', '44', '70'],
		'Appliance Repair': ['2', '3'],
		'Property Management': ['19'],
		'Waste Management': ['19','20'],
		'Pest Control': ['18','23'],
		'Plumbing': ['7', '9', '10', '11', '12', '22', '24', '26', '27', '38']
	}

	if request.method == 'POST':
		subject = {}
		for field in request.form:
			subject[field] = request.form[field]
	g.db = connect_to_database()

	i = (subject['zipcode'],)
	tempbusinesses = g.db.execute("SELECT * FROM business WHERE zipcode=?", i)

	violations = []
	j = jobdict[subject['occupation']]
	for code in j:
		tempviolations = g.db.execute("SELECT * FROM violations WHERE violationnum=?", [code]).fetchall()

		violationspart = [list(row) for row in tempviolations]

		# for row in violationspart:
			# print row
			# violations = violations.append(row)






		# tempviolations = tempviolations.fetchall()
		# print violations
		# for row in tempviolations:
		# 	print row
		# 	cheese = [""] * len(list(row))
		# 	for mold in range(len(list(row))):
		# 		print mold
		# 		cheese[mold] = "" + list(row)[mold]
		# 	violations = violations.append(cheese)
		# 	print cheese
		# 	print violations
		# 	# print list(row)
		# # violations = violations.append([list(row) for row in tempviolations])

		# violations = violations.append(ast.literal_eval(tempvio))
	# businesses = g.db.execute("SELECT * FROM violations WHERE violationnum IN (?)", (j,))
	# businesses = g.db.execute("SELECT * FROM violations WHERE violationnum IN ()")

	businesses = tempbusinesses.fetchall()
	# violations = tempviolations.fetchall()

	result = []
	businesses = [list(row) for row in businesses]
	# violations = [list(row) for row in violations]
	for biz in businesses:
		result.append(biz[0]+" - "+biz[2]+biz[3])
		for vio in violations:
			temp = "" + vio[0]
			if biz[1] == temp:
				result.append("  - "+vio[2])

	print 'started function'
	msg = Message("Your Leads", sender="leads@312LEADS.com", recipients=[subject['email']])
	print 'made email'
	msg.body = ''.join(result)
	# mail.send(msg)
	print 'sent email'

	return render_template('email_dump.html', leads=result)

if __name__ == "__main__":
	app.debug = True
	app.run()
