import imp
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask import request
import psycopg2
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/my_app')
def my_app():
    conn = None
    try:
        conn = psycopg2.connect("dbname=motiv_quote user=vijay password=ryzen host=localhost")
        cur = conn.cursor()
        user = request.args.get('message')
        sql = "INSERT INTO quotes(motivational_message) VALUES(%s)"
        cur.execute(sql, (user,))
        conn.commit()
        cur.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print("connection closed")
        return jsonify([])

@app.route('/get_messages')
def get_messages():
    conn = None
    try:
        conn = psycopg2.connect("dbname=motiv_quote user=vijay password=ryzen host=localhost")
        cursor = conn.cursor()
        sql = "select * from quotes;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        rowarray_list = []
        for row in rows:
            t = { 'message': row[0], 'id': row[1]}
            rowarray_list.append(t)
        conn.commit()
        cursor.close()
        return json.dumps(rowarray_list)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print("connection closed")
    


if __name__ == '__main__':
    app.run(debug=True)




