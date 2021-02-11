from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from views import main
from extensions import db
from models import *

# Initialize flask application
app = Flask(__name__)

# Application configurations
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dispute.db'

# Register blueprint from views
app.register_blueprint(main)

# Initialize socket with flask app
socketio = SocketIO(app)


# Initialize application database
db.init_app(app)

# Database creation
with app.app_context():
    db.create_all()

# Handle user connection to server
@socketio.on('connection')
def handleConnection(name):
	print(name)
	# Send connection data to clients
	socketio.emit('connection-response', name)


# Handle messages
@socketio.on('message')
def handleMessage(data):
	
	name = data['name']
	message = data['message']

	# Make sure fields aren't empty
	if name and message:

		# Add new message to database
		new_message = Message(name=name, message=message)
		try:
			db.session.add(new_message)
			db.session.commit()
		except Exception as e:
			print(e)

		# Send message data to clients
		socketio.emit('message-response', data)

# Run application
if __name__ == '__main__':
	app.run(debug=True)
	socketio.run(app)
