import MySQLdb

from API.Views.Helpers.Connector.Connector import connect


def Update(query, params):
    try:
        connection = connect()
        with connection:
            cursor = connection.cursor()
            connection.begin()
            cursor.execute(query, params)
            connection.commit()
            cursor.close()
            id = cursor.lastrowid
        connection.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Update error")
    return id


def Select(query, params):
    try:
        connection = connect()
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
        connection.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Select error")
    return result