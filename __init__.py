import requests
import sqlite3
import inspect, os


from flask import Flask, render_template, request, g
app = Flask(__name__)

app.database = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/abcproject.db'
def connect_to_database():
	return sqlite3.connect(app.database)

@app.route("/")
def main():
	# g.db = connect_to_database()
	# current = g.db.execute('select * from violations')
	# subjects = current.fetchall()
	# print subjects
	return render_template('index.html')

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
	j = jobdict[subject['occupation']]
	print j
	businesses = g.db.execute("SELECT * FROM business WHERE zipcode=?", i)
	for code in j:
		print code
		violations = g.db.execute("SELECT * FROM violations WHERE violationnum IN (?)", code)
	# businesses = g.db.execute("SELECT * FROM violations WHERE violationnum IN (?)", (j,))
	# businesses = g.db.execute("SELECT * FROM violations WHERE violationnum IN ()")
	leads = violations.fetchall()
	return render_template('email_dump.html', leads=leads)

if __name__ == "__main__":
	app.debug = True
	app.run()
