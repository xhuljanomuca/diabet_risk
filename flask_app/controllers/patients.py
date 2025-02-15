from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models.patient import Patient
from flask_app.models.user import User

TOTAL_QUESTIONS = 15

@app.route('/add/patient')
def start_questionnaire():
    session["questionnaire"] = {}
    return redirect('/add/patient/1')


@app.route('/add/patient/<int:step>', methods=['GET', 'POST'])
def patient_questionnaire(step):
    session.permanent = True 
    if "questionnaire" not in session:
        session["questionnaire"] = {}

    if request.method == "POST":
        session["questionnaire"][f"q{step}"] = request.form.to_dict()
        session.modified = True

        print(f"Saved answer for Q{step}: {session['questionnaire'][f'q{step}']}")
        print(f"Request URL: {request.url}")
        print(f"Redirect Parameter: {request.args.get('redirect')}")

        if "redirect" in request.args and request.args.get("redirect") == "review":
            print("Redirecting back to the review page after editing...")
            return redirect(url_for("review_questionnaire"))

        if step < 15:
            return redirect(url_for("patient_questionnaire", step=step + 1))
        else:
            return redirect(url_for("review_questionnaire"))

    saved_answers = session["questionnaire"].get(f"q{step}", {})

    return render_template(f'question_{step}.html', step=step, saved_answers=saved_answers)


@app.route('/submit_questionnaire', methods=['POST', 'GET'])
def submit_questionnaire():
    print("Checking session data before submission...")

    # Check if the questionnaire session exists
    if "questionnaire" not in session:
        flash("Please complete the questionnaire.", "error")
        print("Error: `session['questionnaire']` is missing!")
        return redirect('/add/patient/1')

    if len(session["questionnaire"]) != 15:
        flash("Incomplete questionnaire! Please answer all questions.", "error")
        print(f"Error: Session contains only {len(session['questionnaire'])} questions instead of 15.")
        print(f"Session data: {session.get('questionnaire')}")
        return redirect('/add/patient/1')

    print(f"Session data before submission: {session['questionnaire']}")

    if "user_id" not in session:
        flash("You need to log in before completing the questionnaire.", "error")
        print("Error: User not logged in!")
        return redirect('/loginPage')

    loggedUserData = {"user_id": session["user_id"]}
    loggedUser = User.get_user_by_id(loggedUserData)

    if not loggedUser:
        flash("Error retrieving user details.", "error")
        print("Error: Logged user not found!")
        return redirect('/loginPage')

    medical_center_id = loggedUser.get("medical_center_id")

    # **Mapping of Points for Each Option**
    points_mapping = {
        "age": {"18-44 years": 0, "45-54 years": 7, "55-64 years": 13, "65-74 years": 15},
        "gender": {"Male": 6, "Female": 0},
        "bmi": {"Less than 25": 0, "25 to 29": 4, "30 to 34": 9, "35 and over": 14},
        "waist_size": {
            "Less than 94 cm for men; or Less than 80 cm for women": 0,
            "Between 94–102 cm; or Between 80–88 cm for women": 4,
            "Over 102 cm for men; or Over 88 cm for women": 6
        },
        "physical_activity": {"Yes": 0, "No": 1},
        "fruit_vegetable_intake": {"Every day": 0, "Not every day": 2},
        "high_blood_pressure": {"Yes": 4, "No": 0},
        "high_sugar_pressure": {"Yes": 14, "No": 0},
        "pregnancy_large_baby": {"Yes": 1, "No": 0},
        "mother_diabetes": {"Yes": 2, "No": 0},
        "father_diabetes": {"Yes": 2, "No": 0},
        "siblings_diabetes": {"Yes": 2, "No": 0},
        "children_diabetes": {"Yes": 2, "No": 0},
        "ethnicity": {"South Asian": 11, "East Asian": 10, "Black": 5, "Aboriginal": 3, "Other non-white": 3, "White": 0},
        "education_level": {"Some high school or less": 5, "High school diploma": 1, "Some college or university": 0, "University or college degree": 0}
    }

    total_score = 0
    data = {}

    # Calculate total score based on user choices
    for step in range(1, 16):
        question_data = session["questionnaire"].get(f"q{step}", {})

        for key, value in question_data.items():
            data[key] = value
            if key in points_mapping and value in points_mapping[key]:
                total_score += points_mapping[key][value]

    data["risk_score"] = total_score
    data["doctor_id"] = session["user_id"]
    data["medical_center_id"] = medical_center_id 

    print(f"Inserting Patient Questionnaire Data: {data}")

    result = Patient.create_patient_questionnaire(data)

    if not result:
        flash("Database error! Please try again.", "error")
        print("Error: Database insertion failed!")
        return redirect('/add/patient/1')

    session.pop("questionnaire", None)
    session["risk_score"] = total_score

    print(f"Successfully calculated risk score: {total_score}")
    print("Redirecting to /show_risk_score")

    flash(f"Patient questionnaire submitted successfully! Risk Score: {total_score}", "success")
    
    return redirect('/show_risk_score')


@app.route('/review_questionnaire')
def review_questionnaire():
    if "questionnaire" not in session:
        flash("Please complete the questionnaire first.", "error")
        return redirect('/add/patient/1')

    saved_answers = session["questionnaire"]

    question_labels = {
        "q1": "Gender",
        "q2": "Age",
        "q3": "BMI",
        "q4": "Waist Size",
        "q5": "Physical Activity",
        "q6": "Fruit and Vegetable Intake",
        "q7": "High Blood Pressure",
        "q8": "High Sugar Pressure",
        "q9": "Pregnancy Large Baby",
        "q10": "Mother Diabetes",
        "q11": "Father Diabetes",
        "q12": "Siblings Diabetes",
        "q13": "Children Diabetes",
        "q14": "Ethnicity",
        "q15": "Education Level",
    }

    return render_template(
        'review_questionnaire.html', 
        saved_answers=saved_answers, 
        question_labels=question_labels
    )



@app.route('/save_answer/<int:step>', methods=['POST'])
def save_answer(step):
    if "questionnaire" not in session:
        session["questionnaire"] = {}

    session["questionnaire"][f"q{step}"] = request.form.to_dict()
    session.modified = True

    print(f"Saved answer for Q{step}: {session['questionnaire'][f'q{step}']}")

    if request.args.get("redirect") == "review":
        return redirect("/review_questionnaire")

    if step < 15:
        return redirect(f"/add/patient/{step + 1}")
    else:
        return redirect("/review_questionnaire")


