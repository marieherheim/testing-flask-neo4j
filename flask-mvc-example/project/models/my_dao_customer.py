from neo4j import GraphDatabase, Driver
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

def save_customer(name, age, address, drivers_licence):
    with _get_connection().session() as session:
        customers = session.run("MERGE (c:Customer{name: $name, age: $age, address: $address, drivers_licence: $drivers_licence}) RETURN c;", name=name, age=age, address=address, drivers_licence=drivers_licence)
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) RETURN c;")
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def findCustomerByName(name):
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) where c.name=$name RETURN c;", name=name)
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def update_customer(name, age, address, drivers_licence):
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer{name:$name}) SET c.age=$age, c.address=$address, c.drivers_licence=$drivers_licence RETURN c;", name=name, age=age, address=address, drivers_licence=drivers_licence)
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def delete_customer(name):
    with _get_connection().session() as session:
        session.run("MATCH (c:Customer{name: $name}) DELETE c;", name=name)
