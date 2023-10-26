from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+s://c6387231.databases.neo4j.io"
AUTH = ("neo4j", "S2OBk4iLfXnoPnRHlIkSzC6IhpjKP2AxcjP05YVE2mo")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

def save_customer(name, age, address):
    with _get_connection().session() as session:
        customers = session.run("MERGE (c:Customer{name: $name, age: $age, address: $address}) RETURN c;", name=name, age=age, address=address)
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

def update_customer(name, age, address):
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer{name:$name}) set c.age=$age, c.address=$address RETURN c;", name=name, age=age, address=address)
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def delete_customer(name):
    with _get_connection().session() as session:
        session.run("MATCH (c:Customer{name: $name}) delete c;", name=name)
