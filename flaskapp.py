from flask import Flask, render_template, request, redirect, url_for, flash
from functioncode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
                                   

@app.route('/')
def home():

    schedule_dictionary = {'Freshman Fall':[], 'Freshman Spring': [], 'Sophomore Fall': [], 'Sophomore Spring': [], 'Junior Fall': [], 'Junior Spring':[], 'Senior Fall': [], 'Senior Spring': []}
    course_planning = Problem()
    creating_variables(get_courses())
    prereq_constraints(get_prereqs())
    singleclass_requirements_constraints(get_cs_requirements())
    multiclass_requirements_constraints(get_cs_requirements())
    credit_limit_constraint()
    solutions = get_solutions(1)

    for x in solutions[0]:
        if solutions[0][x] == 202510:
            schedule_dictionary['Freshman Fall'].append(x)
        if solutions[0][x] == 202520:
            schedule_dictionary['Freshman Spring'].append(x)
        if solutions[0][x] == 202610:
            schedule_dictionary['Sophomore Fall'].append(x)
        if solutions[0][x] == 202620:
            schedule_dictionary['Sophomore Spring'].append(x)
        if solutions[0][x] == 202710:
            schedule_dictionary['Junior Fall'].append(x)
        if solutions[0][x] == 202720:
            schedule_dictionary['Junior Spring'].append(x)
        if solutions[0][x] == 202810:
            schedule_dictionary['Senior Fall'].append(x)
        if solutions[0][x] == 202820:
            schedule_dictionary['Senior Spring'].append(x)

    return render_template('home.html', schedule = schedule_dictionary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)