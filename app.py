from flask import Flask,request,render_template, redirect
from multiprocessing import Process
from zap import Zap

import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    usage = """
     <h1> Simple API ZAP </h1>
     <code>http://api:5000/api?host=https://app_to_test.com</code></br>
     <code>http://api:5000/reports</code></br>
     <code>http://api:5000/reports?report=report_app_to_test.com.html</code</code></br>
    """
    return usage


@app.route('/api')
def analyze():
    host = request.args.get('host')
    zap = Zap(host, debug=True)
    p = Process(target=zap.run())
    p.start()
    #p.join()
    return redirect('/reports')

@app.route('/reports')
def reports():
    report = request.args.get('report')
    conn = sqlite3.connect('running.db')
    c = conn.cursor()
    c.execute("SELECT * FROM running ORDER BY id DESC")
    data = ""
    for d in c.fetchall():
        data = data + " Relatorio: {}.html, Status: {} </br>".format(d[1],d[2])
    conn.commit()
    print(report)
    if report:
        return render_template('reports/' + report)
    
    return data
    

app.run(debug=True)

