from API.Views.Helpers.Connector.Execuror import Select

def find(table, id, value):
    if not len(Select('SELECT id FROM ' + table + ' WHERE ' + id + ' = %s', (value, ))):
        raise Exception("No such element in " + table + " with " + id + " = " + str(value))
    return
