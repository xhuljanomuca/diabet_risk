from flask_app import app
from flask import render_template, redirect, session, request, flash, Response
import json
from flask_app.models.user import User
from flask_app.models.patient import Patient
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/profile') 
    return redirect('/logout') 


@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/login', methods=['POST']) 
def login():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_user_by_email(request.form) 
    if user == False:
        flash('This email does not exist.', 'emailLogIn')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/')


@app.route('/registerPage')
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    cities = User.get_all_cities()
    return render_template('register.html', cities=cities)


@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')

    if User.get_user_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)

    if not User.validate_user(request.form):
        return redirect(request.referrer)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'medical_center_id': request.form['medical_center_id'],
        'confirm_password': request.form['confirm_password']
    }
    User.create_user(data)
    flash('User succefully created', 'userRegister')
    return redirect('/')


@app.route('/profile')
def patients():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(loggedUserData)
    patients = User.getDoctorPatients(loggedUserData)
    if not loggedUser:
        return redirect('/logout')
    return render_template('profile.html', loggedUser=User.get_user_by_id(loggedUserData), patients=Patient.get_all())


@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/loginPage')


@app.route('/edit_profile')
def edit_profile():
    if 'user_id' not in session:
        return redirect('/loginPage')

    loggedUserData = {'user_id': session['user_id']}
    loggedUser = User.get_user_by_id(loggedUserData)
    
    cities = User.get_all_cities()
    medical_centers = User.get_medical_centers_by_city({"city_id": loggedUser["city_id"]})

    return render_template('edit_profile.html', loggedUser=loggedUser, cities=cities, medical_centers=medical_centers)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect('/loginPage')

    data = {
        "doctor_id": session['user_id'],
        "medical_center_id": request.form['medical_center_id']
    }

    User.editDoctorProfile(data)
    flash("Profile updated successfully!", "success")

    return redirect('/profile')


@app.route('/get_medical_centers/<int:city_id>')
def get_medical_centers(city_id):
    data = {"city_id": city_id}
    medical_centers = User.get_medical_centers_by_city(data)

    print(f"Fetched Medical Centers: {medical_centers}")

    if not medical_centers:
        return Response(json.dumps([]), mimetype='application/json')

    return Response(json.dumps(medical_centers), mimetype='application/json')


@app.route('/show_risk_score')
def show_risk_score():
    if "risk_score" not in session:
        return redirect('/profile')  # Redirect if no score exists

    risk_score = session["risk_score"]

    # Determine the risk category
    if 0 <= risk_score <= 32:
        risk_category = "Low to moderate risk"
        risk_chance = "1–17% chance of being diagnosed with diabetes over the next 10 years."
        alert_class = "alert-success"
    elif 33 <= risk_score <= 42:
        risk_category = "High risk"
        risk_chance = "33% chance of being diagnosed with diabetes over the next 10 years."
        alert_class = "alert-warning"
    else:
        risk_category = "Very high risk"
        risk_chance = "50% chance of being diagnosed with diabetes over the next 10 years."
        alert_class = "alert-danger"

    return render_template("risk_score_result.html", risk_score=risk_score, risk_category=risk_category, risk_chance=risk_chance, alert_class=alert_class)
