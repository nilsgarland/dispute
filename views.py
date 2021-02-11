from flask import Blueprint, render_template, request, redirect, session, url_for
from models import *
from datetime import datetime
from extensions import db
import requests

# Create main routing blueprint
main = Blueprint('main', __name__)

## Routes

@main.route('/')
def index():
	# Automatically logout if in session
	if "name" in session:
		session.clear()
	return render_template("index.html")

@main.route('/chat', methods=['GET', 'POST'])
def chat():

	# Retrieve all messages from database
	messages = Message.query.order_by(Message.id).all()

	# Return template with message history
	if request.method == "POST":
		name = request.form['name']
		if name:
			session['name'] = name
			return render_template('chat.html', messages=messages)
		else:
			return redirect(url_for('main.index'))
	else:
		if "name" in session:
			return render_template('chat.html', messages=messages)
		else:
			return redirect(url_for('main.index'))