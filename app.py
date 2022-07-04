from flask import Flask, render_template, request, redirect, url_for
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from threading import Timer
import os
import sys
from flask_sqlalchemy import SQLAlchemy

# Start using all the regular flask logic
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dkstudio.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
db = SQLAlchemy(app)


class MMA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fighter_name = db.Column(db.String(80))
    fighter_points = db.Column(db.Integer)
    fighter_class = db.Column(db.String(80))


class Nascar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(80))
    driver_points = db.Column(db.Integer)
    miles_in_race = db.Column(db.Integer)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mma_entry')
def mma_entry():
    return render_template('mma_entry.html')


@app.route('/add_mma_entry', methods=['POST'])
def add_mma_entry():
    fighter_name = request.form['fighter_name']
    fighter_points = request.form['fighter_points']
    fighter_class = request.form['weight_class']
    new_fighter = MMA(fighter_name=fighter_name, fighter_points=fighter_points, fighter_class=fighter_class)
    db.session.add(new_fighter)
    db.session.commit()
    return redirect(url_for('mma_entry'))


@app.route('/nascar_entry')
def nascar_entry():
    return render_template('nascar_entry.html')


# Define function for QtWebEngine
def ui(location):
    qt_app = QApplication(sys.argv)
    web = QWebEngineView()
    web.setWindowTitle("DK Studio")
    web.resize(1024, 768)
    web.setZoomFactor(1)
    web.load(QUrl(location))
    web.show()
    sys.exit(qt_app.exec_())


if __name__ == "__main__":
    # start sub-thread to open the browser.
    Timer(1, lambda: ui("http://127.0.0.1:5000/")).start()
    db.create_all()
    app.run(debug=True)
