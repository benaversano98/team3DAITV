import mysql.connector
from mysql.connector import Error

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def drop_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database cancelled successfully")
    except Error as err:
        print(f"Error: '{err}'")


def crea_database(connect_server, db_name):
    db = f"CREATE DATABASE IF NOT EXISTS {db_name}"
    create_database(connect_server, db)


def elimina_database(connect_server, db_name):
    db = f"DROP DATABASE IF EXISTS {db_name}"
    drop_database(connect_server, db)


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query, optional=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, optional)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")


def executemany_query(connection, query, optional=None):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, optional)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query, optional=None):
    cursor = connection.cursor()
    # result = None
    try:
        cursor.execute(query, optional)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def readmany_query(connection, query, optional=None):
    cursor = connection.cursor()
    result = []
    try:
        for i in optional:
            cursor.execute(query, i)
            result.extend(cursor.fetchall())
        return result
    except Error as err:
        print(f"Error: '{err}'")


def fk_0(connection):
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    connection.commit()


def fk_1(connection):
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    connection.commit()