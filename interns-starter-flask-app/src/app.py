from crypt import methods
import os
from datetime import datetime
from unittest import result
from flask import Flask, render_template, make_response, jsonify, request
import pymysql
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder='templates')

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
mysql.init_app(app)



def get_app_debug_info():
    cfg_items = {k: v for k, v in os.environ.items()}
    cfg_items['datetime'] = datetime.now().isoformat()
    return cfg_items


@app.route('/')
def welcome():
    return {
        'msg': 'Hello World! This is a simple Python app using Flask! But wait there is more!',
        'endpoints': ['/', '/ping', '/debug', '/debug/ui', '/fetchdb']
    }


@app.route('/ping')
def ping():
    return {'msg': 'pong!'}


@app.route('/debug', methods=['GET'])
def debug():
    cfg_items = get_app_debug_info()
    response = make_response(cfg_items, 200)

    # Enable CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    response.headers['Access-Control-Allow-Origin'] = '*'  # allow all domains for now
    response.headers['Access-Control-Allow-Methods'] = "GET"

    return response


@app.route('/debug/ui', methods=['GET'])
def debug_ui():
    cfg_map = get_app_debug_info()
    # sort items by key
    cfg_items = sorted([{'k': k, 'v': v} for k, v in cfg_map.items()], key=lambda x: x['k'].upper())
    return render_template('debug.html', cfg_items=cfg_items, title='Hello Python Debug!')

@app.route('/fetchdb', methods=['GET'])
def fetch_db():
    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")

    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp

@app.route('/form', methods=['GET'])
def test():
    
    return render_template("form.html")

@app.route('/form', methods=['POST'])
def insert():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    
    cursor.execute("INSERT INTO user (id,name,email,phone,address) VALUES (NULL,%s, %s, %s, %s)" ,(name, email, int(phone), address))
    conn.commit()
    return "Success"

@app.errorhandler(404)
def not_found(e):
    return {'err': 'Not found!'}, 404


if __name__ == '__main__':
    port = os.environ.get('PORT', 5001)
    app.run(debug=True, host='0.0.0.0', port=port)
