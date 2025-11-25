from flask import Flask, render_template, request, redirect 
import mysql.connector
app = Flask(__name__)
@app.route('/')
def index():
    return redirect('/Menu')
@app.route('/Menu')
def menu():
    return render_template('menu.html', title="Menu")
# @app.route('/Characters')
# @app.route('/News')
# @app.route('/Accounts')
# @app.route('/Profile')

