from extensions import db
from datetime import datetime

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	message = db.Column(db.String(200), nullable=False)

	def __repr__(self):
		return '<Message %r>' % self.id