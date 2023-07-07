from flask import Flask, render_template, request
from symptom_diagnosis import diagnose

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def symptom_assessment():
    if request.method == 'POST':
        intensity = request.form['intensity']
        location = request.form['location']
        duration = request.form['duration']
        aggravating_factors = request.form['aggravating_factors']
        alleviating_factors = request.form['alleviating_factors']
        other_symptoms = request.form['other_symptoms']
        previous_treatment = request.form['previous_treatment']
        additional_info = request.form['additional_info']
        # Process the collected information (e.g., store in a database, perform calculations)
        
        return render_template('summary.html',
                               intensity=intensity,
                               location=location,
                               duration=duration,
                               aggravating_factors=aggravating_factors,
                               alleviating_factors=alleviating_factors,
                               other_symptoms=other_symptoms,
                               previous_treatment=previous_treatment,
                               additional_info=additional_info)
    
    return render_template('index.html')

@app.route('/diagnose')
def diagnosis(symptoms,database):
    return diagnose(symptoms, database)

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Change the port number to a different value

