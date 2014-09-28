from flask import Flask
from flask.ext.mail import Mail, Message

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'adam@adamyala.com',
    MAIL_PASSWORD = 'Salim135',
))

mail = Mail(app)

@app.route("/")
def index():
	print 'started function'
	msg = Message("Hello", sender="from@example.com", 
		html="""<table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
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
  <td bgcolor="#333" style="color:white; text-align:center">
  </td>
 </tr>
 <tr>
   <td bgcolor="#333" style="text-align:center; color:#999; padding: 15px 15px 15px 15px;">
    Created at the MonkeyBars Open Build Hackathon
  </td>
</tr>
</table>""",
		recipients=["adamkyala@gmail.com"])
	print 'made email'

	mail.send(msg)
	print 'sent email'
	return

if __name__ == "__main__":
	app.debug = True
	app.run()

