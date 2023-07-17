from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users, posts
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')

class User:
    db="pulse_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.subscribe = data['subscribe']
        self.new_student = data['new_student']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_users(cls):
        query="""
            SELECT * FROM users;
        """
        results = connectToMySQL(cls.db).query_db(query)

        users=[]

        for user in results:
            user.append(cls(user))
        
        return users

#get one user
    @classmethod
    def get_one_user(cls, data):
        query="""
            SELECT * FROM users
            WHERE (id) = %(id)s;
        """
        results= connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

#get user with email
    @classmethod
    def user_with_email(cls, data):
        query="""
            SELECT * FROM users
            WHERE (email) = %(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results)<1:
            return False
        return cls(results[0])

#create

    @classmethod
    def create_user(cls, data):
        query="""
        INSERT INTO users
        (first_name, last_name, email, password, subscribe, new_student)
        VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(subscribe)s, %(new_student)s)
        """

        results = connectToMySQL(cls.db).query_db(query, data)

#read

#update

#delete

#validation for user creation
    @staticmethod
    def validate_user(data):
        is_valid=True
        one_user=User.user_with_email(data)
        if one_user:
            is_valid=False
            flash("User already exsists", "registration")
        if len (data['first_name']) <2:
            is_valid = False
            flash("Name must be at least 2 characters", "registration")
        if len (data['last_name']) <2:
            is_valid = False
            flash("Name must be at least 2 characters", "registration")
        if len (data['email']) == 0:
            is_valid = False
            flash("Email cannot be left empty", "registration")
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Inavlid format", "registration")
        if len (data['password']) <8:
            is_valid = False
            flash("Password must be at least 8 Characters", "registration")
        elif not PASSWORD_REGEX.match(data['password']):
            is_valid = False
            flash("Password must be at least 8 characters long, contain at least one letter, number and special character", "registration")
        if data['password'] !=data['confirm password']:
            is_valid = False
            flash("Passwords must match", "registration")
        return is_valid
