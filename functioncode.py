import requests
import json
from constraint import Problem
from constraint import InSetConstraint
from constraint import SomeInSetConstraint
from collections import Counter
from itertools import islice

course_planning = Problem()

def get_courses():

    course_rotation_url = 'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/course_rotation.json'
    course_rotation_data = requests.get(course_rotation_url).json()
    
    return (course_rotation_data)

def get_cs_requirements():

    cs_requirements_url = 'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/cs_major_requirements.json'
    cs_requirements_data = requests.get(cs_requirements_url).json()

    return(cs_requirements_data)

def get_prereqs():

    prerequisites_url = 'https://raw.githubusercontent.com/ericmanley/S24-CS143AI/main/data/prerequisites_simplified.json'
    prerequisites_data = requests.get(prerequisites_url).json()

    return(prerequisites_data)

def creating_variables(class_list):
  for i in range(len(class_list)):
    semester_list = []
    course = class_list[i]['course']
    for semester in class_list[i]['terms_offered']:
      semester_list.append(semester)
      if len(class_list[i]['terms_offered']) == len(semester_list):
        course_planning.addVariable(course,semester_list)

def prereq_constraint(prereq, course):
    return prereq < course

def prereq_constraints(prereq_list):
  for i in range(len(prereq_list)):
    main_course = prereq_list[i]['course']
    for j in range(len(prereq_list[i]['prerequisites'])):
      prereq_course = prereq_list[i]['prerequisites'][j]
      course_planning.addConstraint(prereq_constraint,[prereq_course,main_course])

def singleclass_requirements_constraints(requirements_list):
  for i in range(len(requirements_list)):
    if len(requirements_list[i]['courses']) == 1:
      course_planning.addConstraint(InSetConstraint,[requirements_list[i]['courses'][0]])

def multiclass_requirements_constraints(requirements_list):
  for i in range(len(requirements_list)):
    if (len(requirements_list[i]['courses']) != 1):
      courses= []
      for j in range(len(requirements_list[i]['courses'])):
        courses.append(requirements_list[i]['courses'][j])
      course_planning.addConstraint(SomeInSetConstraint([202510, 202520, 202610, 202620, 202710, 202720, 202810, 202820], n=requirements_list[i]['num_required'],exact=False),courses)

def credit_limit_constraint(*args):
  semester_list = [202510,202520,202610,202620,202710,202720,202810,202820]
  course_rotation_url = 'https://raw.githubusercontent.com/zoe-zillgitt/CapstoneJson/main/course_rotation.json'
  course_rotation_data = requests.get(course_rotation_url).json()
  courses = []
  
  for i in range(len(course_rotation_data)):
    course = course_rotation_data[i]['course']
    courses.append(course)
  
  def semester_limit(*args):
    semester_counts = Counter(args)
    return all(count <= 6 for count in semester_counts.values())
  
  course_planning.addConstraint(semester_limit, courses)

def get_solutions(number_entered):
  
  solution_iter = course_planning.getSolutionIter()
  solutions = list(islice(solution_iter,number_entered))

  return(solutions)

