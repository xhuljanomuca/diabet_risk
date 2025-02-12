from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.patient import Patient

TOTAL_QUESTIONS = 15  # Update based on actual number of questions

@app.route('/add/patient')
def start_questionnaire():
    session["questionnaire"] = {}  # Reset session data
    return redirect('/add/patient/1')


@app.route('/add/patient/<int:step>', methods=['GET', 'POST'])
def patient_questionnaire(step):
    if step < 1 or step > 15:
        return redirect('/profile')

    if request.method == "POST":
        # ✅ Store the answer in session
        session["questionnaire"][f"q{step}"] = request.form.get("answer")

        # ✅ Redirect to the next question
        return redirect(f"/add/patient/{step + 1}")

    return render_template(f'question_{step}.html', step=step)


@app.route('/submit_questionnaire', methods=['POST', 'GET'])
def submit_questionnaire():
    if "questionnaire" not in session or len(session["questionnaire"]) != TOTAL_QUESTIONS:
        flash("Please complete the questionnaire.", "error")
        return redirect('/add/patient')

    data = {
        "gender": session["questionnaire"]["q1"],
        "age": session["questionnaire"]["q2"],
        "waist_size": session["questionnaire"]["q3"],
        "bmi": session["questionnaire"]["q4"],
        "physical_activity": session["questionnaire"]["q5"],
        "fruit_vegetable_intake": session["questionnaire"]["q6"],
        "high_blood_pressure": session["questionnaire"]["q7"],
        "high_sugar_pressure": session["questionnaire"]["q8"],
        "pregnancy_large_baby": session["questionnaire"]["q9"],
        "mother_diabetes": session["questionnaire"]["q10"],
        "father_diabetes": session["questionnaire"]["q11"],
        "siblings_diabetes": session["questionnaire"]["q12"],
        "children_diabetes": session["questionnaire"]["q13"],
        "ethnicity": session["questionnaire"]["q14"],
        "education_level": session["questionnaire"]["q15"],
        "doctor_id": session["user_id"]
    }

    Patient.create_patient_questionnaire(data)
    session.pop("questionnaire", None)  # Clear session after submission
    flash("Patient questionnaire submitted successfully!", "success")
    
    return redirect('/profile')
