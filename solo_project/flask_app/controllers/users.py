from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('/pulse_home.html')

@app.route('/register_page.html')
def register_page():
    return render_template('/register_page.html')