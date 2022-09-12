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


@app.route('/my_app', methods= ['POST'])
def my_app():
    conn = None
    if request.method == 'POST':
        try:
            conn = psycopg2.connect("dbname=dffq9f51m6tqk1 user=whndlakocngjjh password=b66e723bad5ac79859e70ebf32ff19524bd5e2641e156e8e5bdfddcb5a21710a host=ec2-44-205-63-142.compute-1.amazonaws.com")
            
            data = request.get_json()
            motivational_message = data['message']
            #conn = psycopg2.connect("dbname=motiv_quote user=vijay password=ryzen host=localhost")
            cur = conn.cursor()
            sql = 'INSERT INTO quotes(motivational_message, created_at) VALUES(%s, now())'
            cur.execute(sql, (motivational_message,))
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
        conn = psycopg2.connect("dbname=dffq9f51m6tqk1 user=whndlakocngjjh password=b66e723bad5ac79859e70ebf32ff19524bd5e2641e156e8e5bdfddcb5a21710a host=ec2-44-205-63-142.compute-1.amazonaws.com")
        #conn = psycopg2.connect("dbname=motiv_quote user=vijay password=ryzen host=localhost")
        cursor = conn.cursor()
        sql = "select * from quotes;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        rowarray_list = []
        for row in rows:
            t = { 'message': row[1], 'id': row[0]}
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

