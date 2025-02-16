from flask_app.config.mysqlconnection import connectToMySQL
import datetime
import re 
from flask import flash


class Patient:
    def __init__(self, data):
        self.id = data['id']
        self.gender = data['gender']
        self.age = data['age']
        self.waist_size = data['waist_size']
        self.bmi = data['bmi']
        self.physical_activity = data['physical_activity']
        self.fruit_vegetable_intake = data['fruit_vegetable_intake']
        self.high_blood_pressure = data['high_blood_pressure']
        self.high_sugar_pressure = data['high_sugar_pressure']
        self.pregnancy_large_baby = data['pregnancy_large_baby']
        self.mother_diabetes = data['mother_diabetes']
        self.father_diabetes = data['father_diabetes']
        self.siblings_diabetes = data['siblings_diabetes']
        self.children_diabetes = data['children_diabetes']
        self.ethnicity = data['ethnicity']
        self.education_level = data['education_level']
        self.risk_score = data['risk_score']
        self.created_at = data['created_at']

    db_name = 'diabet_risk'

    @classmethod
    def get_patient_by_id(cls, data):
        query = 'SELECT * FROM patient_questionnaire WHERE id= %(patient_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False


    @classmethod
    def get_all(cls, data):
        query = """
                SELECT patient_questionnaire.id, patient_questionnaire.gender, patient_questionnaire.age, 
               patient_questionnaire.bmi, patient_questionnaire.waist_size, 
               patient_questionnaire.physical_activity, patient_questionnaire.fruit_vegetable_intake, 
               patient_questionnaire.high_blood_pressure, patient_questionnaire.high_sugar_pressure, 
               patient_questionnaire.pregnancy_large_baby, patient_questionnaire.mother_diabetes, 
               patient_questionnaire.father_diabetes, patient_questionnaire.siblings_diabetes, 
               patient_questionnaire.children_diabetes, patient_questionnaire.ethnicity, 
               patient_questionnaire.education_level, patient_questionnaire.risk_score, 
               doctor.first_name as doctor_first_name, doctor.last_name as doctor_last_name 
                FROM patient_questionnaire 
                LEFT JOIN doctor ON patient_questionnaire.doctor_id = doctor.id 
                WHERE patient_questionnaire.doctor_id = %(doctor_id)s;
            """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        patients = []
        if results:
            for patient in results:
                patients.append(patient)
        return patients


    @classmethod
    def create_patient_questionnaire(cls, data):
        query = "INSERT INTO patient_questionnaire (gender, age, waist_size, bmi, physical_activity, fruit_vegetable_intake, high_blood_pressure, high_sugar_pressure, pregnancy_large_baby, mother_diabetes, father_diabetes, siblings_diabetes, children_diabetes, ethnicity, education_level, risk_score, doctor_id, created_at, medical_center_id) VALUES (%(gender)s, %(age)s, %(waist_size)s, %(bmi)s, %(physical_activity)s, %(fruit_vegetable_intake)s, %(high_blood_pressure)s, %(high_sugar_pressure)s, %(pregnancy_large_baby)s, %(mother_diabetes)s, %(father_diabetes)s, %(siblings_diabetes)s, %(children_diabetes)s, %(ethnicity)s, %(education_level)s, %(risk_score)s, %(doctor_id)s, now(), %(medical_center_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @staticmethod
    def validate_patient(r):
        is_valid = True
        if not r['gender']:
            flash('Gender field is required', 'gender')
            is_valid = False
        if not r['age']:
            flash('Age field is required', 'age')
            is_valid = False
        if r['age']:
            if int(r['age']) < 25:
                flash('Age can not be less then 25', 'age')
                is_valid = False
            if int(r['age']) > 100:
                flash('Age can not be more then 100', 'age')
                is_valid = False
        if not r['waist_size']:
            flash('Waist size field is required', 'waist_size')
            is_valid = False
        if not r['physical_activity']:
            flash('Physical activity field is required', 'physical_activity')
            is_valid = False
        if not r['fruit_vegetable_intake']:
            flash('Fruit and vegetable intake field is required', 'fruit_vegetable_intake')
            is_valid = False
        if not r['high_blood_pressure']:
            flash('High blood pressure field is required', 'high_blood_pressure')
            is_valid = False
        if not r['high_sugar_pressure']:
            flash('High sugar pressure field is required', 'high_sugar_pressure')
            is_valid = False
        if r['gender'] == 'Female':
            if not r['pregnancy_large_baby']:
                flash('Pregnancy large baby field is required', 'pregnancy_large_baby')
                is_valid = False
        if not r['mother_diabetes']:
            flash('Mother diabetes field is required', 'mother_diabetes')
            is_valid = False
        if not r['father_diabetes']:
            flash('Father diabetes field is required', 'father_diabetes')
            is_valid = False
        if not r['siblings_diabetes']:
            flash('Siblings diabetes field is required', 'siblings_diabetes')
            is_valid = False
        if not r['children_diabetes']:
            flash('Children diabetes field is required', 'children_diabetes')
            is_valid = False
        if not r['ethnicity']:
            flash('Ethnicity field is required', 'ethnicity')
            is_valid = False
        if not r['education_level']:
            flash('Education level field is required', 'education_level')
            is_valid = False
        return is_valid