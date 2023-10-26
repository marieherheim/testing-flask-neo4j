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

def save_employee(employee_id, name, address, branch):
    with _get_connection().session() as session:
        employees = session.run("MERGE (e:Employee{employee_id: $employee_id, name: $name, address: $address, branch: $branch}) RETURN e;", employee_id=employee_id, name=name, address=address, branch=branch)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) RETURN e;")
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def findEmployeeById(employee_id):
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) where e.employee_id=$employee_id RETURN e;", employee_id=employee_id)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def update_employee(employee_id, name, address, branch):
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee{employee_id:$employee_id}) set e.name=$name, e.address=$address, e.branch=$branch RETURN e;", employee_id=employee_id, name=name, address=address, branch=branch)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def delete_employee(employee_id):
    with _get_connection().session() as session:
        session.run("MATCH (e:Employee{employee_id: $employee_id}) delete e;", employee_id=employee_id)
