import MySQLdb

def connect():
     return MySQLdb.connect(host='localhost', port=3306, db='DBForums',
                         user='root', passwd='123',
                         charset='utf8')