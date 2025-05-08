import requests
import json
from constraint import Problem
from constraint import InSetConstraint
from constraint import SomeInSetConstraint
from collections import Counter
from itertools import islice


def reset_course_planning():
    global course_planning
    course_planning = Problem()

course_planning = Problem()

def get_courses(url):

    course_rotation_url = url
    course_rotation_data = requests.get(course_rotation_url).json()
    
    return (course_rotation_data)

def get_requirements(url):

    requirements_url = url
    requirements_data = requests.get(requirements_url).json()

    return(requirements_data)

def get_prereqs(url):

    prerequisites_url = url
    prerequisites_data = requests.get(prerequisites_url).json()

    return(prerequisites_data)

def creating_variables(class_list):
  for i in range(len(class_list)):
    semester_list = []
    course = class_list[i]['course']
    for semester in class_list[i]['terms_offered']:
      semester_list.append(semester)
      if len(class_list[i]['terms_offered']) == len(semester_list):
        try:
          print(course)
          course_planning.addVariable(course,semester_list)
        except ValueError as e:
          print(f"Skipping duplicate or invalid variable '{course}': {e}")

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
      course = requirements_list[i]['courses'][0]
      course_planning.addConstraint(SomeInSetConstraint([202510, 202520, 202610, 202620, 202710, 202720, 202810, 202820], n=requirements_list[i]['num_required'],exact=True),[course])

def multiclass_requirements_constraints(requirements_list):
  for i in range(len(requirements_list)):
    if (len(requirements_list[i]['courses']) != 1):
      courses= []
      for j in range(len(requirements_list[i]['courses'])):
        courses.append(requirements_list[i]['courses'][j])
      course_planning.addConstraint(SomeInSetConstraint([202510, 202520, 202610, 202620, 202710, 202720, 202810, 202820], n=requirements_list[i]['num_required'],exact=False),courses)

def credit_limit_constraint(url):
  semester_list = [202510,202520,202610,202620,202710,202720,202810,202820]
  course_rotation_url = url
  course_rotation_data = requests.get(course_rotation_url).json()
  courses = []

  for i in range(len(course_rotation_data)):
    course = course_rotation_data[i]['course']
    courses.append(course)
  print(courses)

  def semester_limit(*args):
    semester_counts = Counter(args)
    return all(count <= 6 for count in semester_counts.values())

  course_planning.addConstraint(semester_limit, courses)

def get_solutions(number_entered):
  
  solution_iter = course_planning.getSolutionIter()
  solutions = list(islice(solution_iter,number_entered))

  return(solutions)

