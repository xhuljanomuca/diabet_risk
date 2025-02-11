
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.medical_center = data['medical_center']
        self.city = data['city']
        self.created_at = data['created_at']


    db_name = 'diabet_risk'

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM doctors WHERE email= %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM doctors WHERE id= %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM doctors;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO doctors (first_name, last_name, email, password, medical_center, city) VALUES ( %(first_name)s, %(last_name)s,%(email)s,%(password)s, %(medical_center)s, %(city)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = "UPDATE doctors SET email = %(email)s, medical_center = %(medical_center)s, city = %(city)s WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM doctors WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getDoctorPatients(cls, data):
        query = "SELECT patient_questionnaires.id as id from patient_questionnaire where doctor_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        patients = []
        if results:
            for patient in results:
                patients.append(patient['id'])
            return patients
        return patients

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be more or equal to 8 characters', 'password')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match',  'passwordConfirm')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user_update(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['medical_center']) < 2:
            flash('Medical center must be more than 2 characters', 'medicalCenter')
            is_valid = False
        if len(user['city']) < 2:
            flash('City must be more than 2 characters', 'city')
            is_valid = False
        return is_valid
