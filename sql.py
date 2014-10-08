import sqlite3
import inspect, os
from flask import Flask, render_template, request, g

app = Flask(__name__)

with app.app_context():

	app.database = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/abcproject.db'
	def connect_to_database():
		return sqlite3.connect(app.database)

	g.db = connect_to_database()

	code = ('11','26')

	# print map(str,code)

	sql="SELECT * FROM violations WHERE violationnum IN " + str(code) 
	# in_p=', '.join(list(map(lambda x: '%s', code)))
	# in_p = list(map(lambda x: '%s', code))
	# sql = sql % in_p
	print sql
	violations = g.db.execute(sql)

	# violations = g.db.execute("SELECT * FROM violations WHERE violationnum IN ?",('11'))

	# violations = g.db.execute("SELECT * FROM violations WHERE violationnum IN (?)", code)
			     # g.db.execute("SELECT * FROM business WHERE zipcode=?",[i])

	results = violations.fetchall()

	print results