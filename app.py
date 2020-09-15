from flask import Flask,request,render_template, redirect
from database import Database
import subprocess
import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def analyze():
    host = request.args.get('host')
    command = (['python', 'zap.py', '--url', host])
    subprocess.Popen(command)
    response = { 'status':200 }
    return json.dumps(response)

@app.route('/reports')
def reports():
    report = request.args.get('report')
    if report:
        return render_template('reports/' + report)
    else:
        database = Database()
        data = database.get_reports()
        response = {
            'status' : 200,
            'data': []
        }
        database.__exit__()
        for da in data:
            response['data'].append({
                'app' : da[0],
                'status' : da[1]
            })
        response = json.dumps(response)
        return response
    

app.run()

