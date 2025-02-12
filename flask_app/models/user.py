
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
        self.medical_center = data['medical_center_id']
        self.created_at = data['created_at']


    db_name = 'diabet_risk'

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM doctor WHERE email= %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT doctor.*, medical_center.id as medical_center_id, medical_center.medical_center AS medical_center_name, city.id as city_id, city.city AS city_name FROM doctor LEFT JOIN medical_center ON doctor.medical_center_id = medical_center.id LEFT JOIN city ON medical_center.city_id = city.id WHERE doctor.id= %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM doctor;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO doctor (first_name, last_name, email, password, medical_center_id, created_at) VALUES ( %(first_name)s, %(last_name)s,%(email)s,%(password)s, %(medical_center_id)s, now());"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def editDoctorProfile(cls, data):
        query = "UPDATE doctor SET medical_center_id = %(medical_center_id)s WHERE id = %(doctor_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM doctor WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getDoctorPatients(cls, data):
        query = """SELECT 
            patient_questionnaire.id,
            patient_questionnaire.gender,
            patient_questionnaire.age,
            patient_questionnaire.bmi,
            patient_questionnaire.waist_size,
            patient_questionnaire.physical_activity,
            patient_questionnaire.fruit_vegetable_intake,
            patient_questionnaire.high_blood_pressure,
            patient_questionnaire.high_sugar_pressure,
            patient_questionnaire.pregnancy_large_baby,
            patient_questionnaire.mother_diabetes,
            patient_questionnaire.father_diabetes,
            patient_questionnaire.siblings_diabetes,
            patient_questionnaire.children_diabetes,
            patient_questionnaire.ethnicity,
            patient_questionnaire.education_level,
            patient_questionnaire.risk_score,
            doctor.first_name as doctor_first_name,
            doctor.last_name as doctor_last_name
        FROM patient_questionnaire
        LEFT JOIN doctor ON patient_questionnaire.doctor_id = doctor.id
        WHERE patient_questionnaire.doctor_id = %(user_id)s;"""
        
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
        return is_valid
    

    @classmethod
    def get_all_cities(cls):
        query = "SELECT * FROM city;"
        return connectToMySQL(cls.db_name).query_db(query)

    @classmethod
    def get_medical_centers_by_city(cls, data):
        query = "SELECT id, medical_center FROM medical_center WHERE city_id = %(city_id)s;"
        
        print(f"Running Query: {query} with city_id={data['city_id']}")
        
        results = connectToMySQL(cls.db_name).query_db(query, data)

        print(f"Query Results: {results}")

        if not results:
            return []

        return results

