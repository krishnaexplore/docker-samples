from typing import List, Dict
from flask import Flask
import mysql.connector
import json
from flask import request
from flask import Response

app = Flask(__name__)



def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM favorite_colors')
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()

    return results

@app.route('/init')
def init():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS USERDB")
    cursor.execute("CREATE DATABASE USERDB")
    cursor.execute("USE USERDB")
    sql = """CREATE TABLE users (
         ID int,
         USER char(30)
     )"""
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    return "DB Init done"

@app.route("/users/add", methods=['POST'])
def add_users():
    req_json = request.get_json()
    config = {
      'user': 'root',
      'password': 'root',
      'host': 'db',
      'port': '3306'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO USERDB.users (ID, USER) VALUES (%s,%s)", (req_json['uid'], req_json['user']))
    connection.commit()
    cursor.close()
    connection.close()
    return Response("Added", status=200, mimetype='application/json')

@app.route('/users/<uid>')
def get_users(uid):
    #hash = hashlib.sha224(str(uid)).hexdigest()
    #key = "sql_cache:" + hash

    #if (R_SERVER.get(key)):
    #    return R_SERVER.get(key) + "(c)"
    #else:
    print ('input value ')
    print  (uid)
    print ('input value ')
    config = {
      'user': 'root',
      'password': 'root',
      'host': 'db',
      'port': '3306'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("select USER from USERDB.users where ID=" + str(uid))
    data = cursor.fetchone()
    cursor.close()
    connection.close()

    if(data):
        return json.dumps({'user':data[0],'id':uid})
    else:
        return json.dumps({'no': 'records'})
    #if data:
    #        R_SERVER.set(key,data[0])
    #        R_SERVER.expire(key, 36);
    #        return R_SERVER.get(key)
    #    else:
    #        return "Record not found"


@app.route('/')
def index() -> str:
    #return json.dumps({'favorite_colors': favorite_colors()})
    return "ready"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
