from flask import Flask, render_template, request, redirect, url_for, flash,session
from functioncode import *
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
                                   

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        major = request.form.get("major")
        major_2nd = request.form.get("2nd-major")
        minor = request.form.get("minor")

        reset_course_planning()
        course_planning = Problem()

        if major == '':
            return render_template('home.html')
        else:
            creating_variables(get_courses(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major}_course_rotation.json'))
            prereq_constraints(get_prereqs(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major}_prerequisites.json'))
            singleclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major}_major_requirements.json'))
            multiclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major}_major_requirements.json'))

            if major_2nd != '' and major_2nd != major:

                creating_variables(get_courses(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major_2nd}_course_rotation.json'))
                prereq_constraints(get_prereqs(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major_2nd}_prerequisites.json'))
                singleclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major_2nd}_major_requirements.json'))
                multiclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{major_2nd}_major_requirements.json'))

                if minor != '':

                    creating_variables(get_courses(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_course_rotation.json'))
                    prereq_constraints(get_prereqs(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_prerequisites.json'))
                    singleclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_minor_requirements.json'))
                    multiclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_minor_requirements.json'))

            elif minor != '':

                creating_variables(get_courses(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_course_rotation.json'))
                prereq_constraints(get_prereqs(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_prerequisites.json'))
                singleclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_minor_requirements.json'))
                multiclass_requirements_constraints(get_requirements(f'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/{minor}_minor_requirements.json'))
        
        credit_limit_constraint(course_planning._variables)
        schedule_dictionary = OrderedDict([('Freshman Fall', []),('Freshman Spring', []),('Sophomore Fall', []),('Sophomore Spring', []),('Junior Fall', []),('Junior Spring', []),('Senior Fall', []),('Senior Spring', [])])
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

        session['schedule'] = schedule_dictionary
        return redirect(url_for('schedule'))
    else:
        return render_template('home.html')

@app.route('/schedule')
def schedule():
    schedule_dictionary = session.get('schedule',{})
    return render_template('schedule.html',schedule=schedule_dictionary)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)