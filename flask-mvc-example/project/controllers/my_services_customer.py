from project import app
from flask import render_template, request, redirect, url_for
import json
from project.models.my_dao_customer import * 

# get all customers
@app.route('/get_customers', methods=['GET'])
def query_records_customers():
    return findAllCustomers()

# get a customer by name
@app.route('/get_customer_by_name', methods=['POST'])
def find_customer_by_name():
    record = json.loads(request.data)
    return findCustomerByName(record['name'])

# save customer
@app.route('/save_customer', methods=["POST"])
def save_customer_info():
    record = json.loads(request.data)
    return save_customer(record['name'], record['age'], record['address'], record["drivers_licence"])

# update a customer's information by name
@app.route('/update_customer', methods=['PUT'])
def update_customer_info():
    record = json.loads(request.data)
    return update_customer(record['name'], record['age'], record['address'])

# delete a customer by name
@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    record = json.loads(request.data)
    delete_customer(record['name'])
    return findAllCustomers()
