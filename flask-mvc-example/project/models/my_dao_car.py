from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+s://neo4j@dcb0dbcc.databases.neo4j.io"
AUTH = ("neo4j", "L_2jcKHhY8zKU9sMAJpapHAXmsMfDNFfkJfZeTns2yY")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

def save_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MERGE (a:Car{make: $make, model: $model, reg: $reg, year: $year, capacity:$capacity}) RETURN a;", make=make, model=model, reg=reg, year=year, capacity=capacity)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def findCarByReg(reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def update_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.capacity = $capacity RETURN a;", reg=reg, make=make, model=model, year=year, capacity=capacity)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def delete_car(reg):
    with _get_connection().session() as session:
        session.run("MATCH (a:Car{reg: $reg}) delete a;", reg=reg)

def link_customer_to_car(name, reg):
    with _get_connection().session() as session:
        # check if the customer has booked another car
        booked_car = session.run(
            "MATCH (c:Customer{name: $name})-[r:ORDERED]->(a:Car) RETURN a;",
            name=name
        ).single()

        if booked_car:
            return "Customer has already booked a car!"

        # check if the car is available
        car_status = session.run(
            "MATCH (a:Car{reg: $reg}) RETURN a.status AS status", 
            reg=reg
        ).single()

        if not car_status or car_status['status'] != "available":
            return "Car is not available for booking!"

        # link customer to car and change car status to 'booked'
        session.run(
            "MATCH (c:Customer{name: $name}), (a:Car{reg: $reg}) MERGE (c)-[r:ORDERED]->(a) SET a.status = 'booked' RETURN r;",
            name=name, reg=reg
        )

        return "Car booked successfully!"

def unlink_customer_from_car(name, reg):
    with _get_connection().session() as session:
        # Check if the customer has booked the given car
        booked_car = session.run(
            "MATCH (c:Customer{name: $name})-[r:ORDERED]->(a:Car{reg: $reg}) RETURN r;",
            name=name, reg=reg
        ).single()

        if not booked_car:
            return "Customer hasn't booked this car!"

        # Remove the relationship and change car status to 'available'
        session.run(
            "MATCH (c:Customer{name: $name})-[r:ORDERED]->(a:Car{reg: $reg}) DELETE r SET a.status = 'available';",
            name=name, reg=reg
        )

        return "Booking canceled and car is now available!"

def rent_car_for_customer(name, reg):
    with _get_connection().session() as session:
        # Check if the customer has booked the given car
        booked_car = session.run(
            "MATCH (c:Customer{name: $name})-[r:ORDERED]->(a:Car{reg: $reg}) RETURN a.status as status;",
            name=name, reg=reg
        ).single()

        if not booked_car or booked_car["status"] != "booked":
            return "Customer either hasn't booked this car or the car isn't available for rent!"

        # Change the car's status to 'rented'
        session.run(
            "MATCH (a:Car{reg: $reg}) SET a.status = 'rented';",
            reg=reg
        )

        return "Car is now rented!"

def return_car_to_system(name, reg, status):
    # Ensure that the status is valid
    if status not in ['available', 'damaged']:
        return "Invalid status provided!"

    with _get_connection().session() as session:
        # Check if the customer has rented the given car
        rented_car = session.run(
            "MATCH (c:Customer{name: $name})-[r:ORDERED]->(a:Car{reg: $reg}) WHERE a.status = 'rented' RETURN a;",
            name=name, reg=reg
        ).single()

        if not rented_car:
            return "Customer hasn't rented this car or the car is not currently rented!"

        # Update the car's status to the provided value ('available' or 'damaged')
        session.run(
            "MATCH (a:Car{reg: $reg}) SET a.status = $status;",
            reg=reg, status=status
        )

        return f"Car is now {status}!"
