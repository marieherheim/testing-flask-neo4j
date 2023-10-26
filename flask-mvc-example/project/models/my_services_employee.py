from project import app
from flask import render_template, request, redirect, url_for
import json
from project.models.my_dao_employee import *

# get employees
@app.route('/get_employees', methods=['GET'])
def query_records():
    return findAllEmployees()

# get an employee by employee_id
@app.route('/get_employee_by_id', methods=['POST'])
def find_employee_by_id():
    record = json.loads(request.data)
    return findEmployeeById(record['employee_id'])

# save employee
@app.route('/save_employee', methods=["POST"])
def save_employee_info():
    record = json.loads(request.data)
    return save_employee(record['employee_id'], record['name'], record['address'], record['branch'])

# update an employee's information by employee_id
@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    record = json.loads(request.data)
    return update_employee(record['employee_id'], record['name'], record['address'], record['branch'])

# delete an employee by employee_id
@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = json.loads(request.data)
    delete_employee(record['employee_id'])
    return findAllEmployees()
