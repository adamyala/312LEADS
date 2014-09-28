from flask import Flask
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

@app.route("/")
def index():
	print 'started function'
	msg = Message("Hello", sender="from@example.com", recipients=["adamkyala@gmail.com"])
	print 'made email'
	mail.send(msg)
	print 'sent email'
	return

if __name__ == "__main__":
	app.debug = True
	app.run()

