from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

