from flask import Flask, render_template, request, redirect, url_for
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from threading import Timer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
import sys

# Start using all the regular flask logic
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dkstudio.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
db = SQLAlchemy(app)


class Fighter(db.Model):
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
    fighters = Fighter.query.all()
    return render_template('mma_entry.html', fighters=fighters)


@app.route('/add_mma_entry', methods=['POST'])
def add_mma_entry():
    fighter_name = request.form['fighter_name']
    fighter_points = request.form['fighter_points']
    fighter_class = request.form['weight_class']
    new_fighter = Fighter(fighter_name=fighter_name, fighter_points=fighter_points, fighter_class=fighter_class)
    db.session.add(new_fighter)
    db.session.commit()
    return redirect(url_for('mma_entry'))


@app.route('/delete_fighter_entry/<int:fighter_id>')
def delete_fighter_entry(fighter_id):
    Fighter.query.filter_by(id=fighter_id).delete()
    db.session.commit()
    return redirect(url_for('mma_entry'))


@app.route('/nascar_entry')
def nascar_entry():
    drivers = Nascar.query.all()
    return render_template('nascar_entry.html', drivers=drivers)


@app.route('/add_nascar_entry', methods=['POST'])
def add_nascar_entry():
    driver_name = request.form['driver_name']
    driver_points = request.form['driver_points']
    miles_in_race = request.form['miles_in_race']
    new_driver = Nascar(driver_name=driver_name, driver_points=driver_points, miles_in_race=miles_in_race)
    db.session.add(new_driver)
    db.session.commit()
    return redirect(url_for('nascar_entry'))


@app.route('/delete_driver_entry/<int:driver_id>')
def delete_driver_entry(driver_id):
    Nascar.query.filter_by(id=driver_id).delete()
    db.session.commit()
    return redirect(url_for('nascar_entry'))


@app.route('/optimal')
def optimal():
    fighters = Fighter.query.order_by(desc(Fighter.fighter_points))
    drivers = Nascar.query.order_by(desc(Nascar.driver_points))
    return render_template('optimal.html', fighters=fighters, drivers=drivers)


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
