import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
db = 'login_registration'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.dob = data['dob']
        self.password = data['password']
        self.fav_language = data['fav_language']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Validate user
    @staticmethod
    def user_validator(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[0-9]).{8,}')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters!', 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email!', 'register')
            is_valid = False
        query = """
                SELECT * FROM users WHERE email = %(email)s
                """
        results = connectToMySQL(db).query_db(query,data)
        if len(results) != 0:
            flash('This email is already being used!', 'register')
            is_valid = False
        if len(data['dob']) < 1:
            flash('Please select your birthday!', 'register')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash('Password must be at least 8 characters, with 1 number and 1 uppercase letter!', 'register')
            is_valid = False
        if data['password'] != data['confirm_pw']:
            flash('Password does not match!', 'register')
            is_valid = False
        if len(data['fav_language']) < 1:
            flash('Please select your favorite programming language!', 'register')
            is_valid = False
        return is_valid

    # Setup query to create user
    @classmethod
    def create_user(cls,data):
        query = """
                INSERT INTO users (first_name, last_name, email, dob, password, fav_language, created_at, updated_at)
                VALUE (%(first_name)s, %(last_name)s, %(email)s, %(dob)s, %(pw_hash)s, %(fav_language)s, NOW(), NOW())
                """
        return connectToMySQL(db).query_db(query,data)
    
    # Setup query to login user
    @classmethod
    def get_by_email(cls,data):
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s
                """
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        print(results)
        return (cls(results[0]))

    # Get one user by ID
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
                """
        return connectToMySQL(db).query_db(query,data)