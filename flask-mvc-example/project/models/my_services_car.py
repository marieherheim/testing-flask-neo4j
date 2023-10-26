from project import app
from flask import render_template, request, redirect, url_for
import json 
from project.models.my_dao_car import * 

# get cars
@app.route('/get_cars', methods=['GET'])
def query_records():
    return findAllCars()

# use registration number to find the car object from database
@app.route('/get_cars_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
    record = json.loads(request.data)
    print(record)
    return findCarByReg(record['reg'])

# save car
@app.route('/save_car', methods=["POST"])
def save_car_info():
    record = json.loads(request.data)
    print(record)
    return save_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

# update car information
@app.route('/update_car', methods=['PUT'])
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

# deletes car by removing the records
@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)
    print(record)
    delete_car(record['reg'])
    return findAllCars()

# order a car
@app.route('/order-car', methods=['POST'])
def order_car():
    data = json.loads(request.data)
    name = data.get('name')
    reg = data.get('reg')
    result = link_customer_to_car(name, reg)
    return result

# cancel order of a car
@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = json.loads(request.data)
    name = data.get('name')
    reg = data.get('reg')
    result = unlink_customer_from_car(name, reg)
    return result

# rent a car
@app.route('/rent-car', methods=['POST'])
def rent_car():
    data = json.loads(request.data)
    name = data.get('name')
    reg = data.get('reg')
    result = rent_car_for_customer(name, reg)
    return result

# return a car
@app.route('/return-car', methods=['POST'])
def return_car():
    data = json.loads(request.data)
    name = data.get('name')
    reg = data.get('reg')
    status = data.get('status')  # This can be 'available' or 'damaged'
    result = return_car_to_system(name, reg, status)
    return result
