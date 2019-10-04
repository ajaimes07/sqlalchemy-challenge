# Author: Aline Jaimes
# Date: 10/02/19
# Name: ClimateApp
# Goal: Design a Flask API based on the climate exploratory analysis.

#1 Import Dependencies
import sqlalchemy
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
Base= automap_base()
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
from flask import Flask, jsonify
# 2 Database Setup
#a. engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn= engine.connect()
#b.  reflect an existing database into a new model
Base = automap_base()
# c. reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
# d. Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# 3. Flask Setup
# a. Create an app, being sure to pass __name__
app = Flask(__name__)
# c. Define what to do when a user hits the index route
@app.route("/")
def Welcome():
    """List all available api routes."""
    return(
        f"Welcome to the Hawaii Climate App!<br/>" 
        f"Here is a list of available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/end_date to query for a period of time. Formating yyyy-mm-dd. Example: 2016-05-15/2016-05-30<br/>"
    )
# d. Define what to do when a user hits the / routes
@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
    #print("Server received request for 'Precipitation' page...")
    #return "Here is a list of the last 12 months of precipitation in Hawaii"
    #retrieve the last 12 months of precipitation data
    qr1=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    qr2=dt.date(2017,8,23)-dt.timedelta(days=365)
    ppt=session.query(Measurement.prcp,Measurement.date).\
    filter(Measurement.date > qr2).\
    order_by(Measurement.date).all()
    session.close
 # e. Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    precipitation=[]
    for date, prcp in ppt:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)
# f. Return the JSON representation of your dictionary.
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stnsNo=session.query(Measurement.station,func.count(Measurement.station).label('count')).\
group_by(Measurement.station).all()
    session.close
    return jsonify(stnsNo)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    qr1=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    qr2=dt.date(2017,8,23)-dt.timedelta(days=365)
    TA=session.query(Measurement.tobs,Measurement.date).\
    filter(Measurement.date > qr2).\
    order_by(Measurement.date).all()
    session.close()
    #Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    AT=[]
    for date,tobs in TA:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        AT.append(tobs_dict)
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(AT)
#@app.route("/api/v1.0/start_date/end_date to query for a period of time. Formating yyyy-mm-dd. Example: 2016-05-15/2016-05-30")
@app.route("/api/v1.0/start_date/end_date")
def start_end(start_date, end_date):
    session = Session(engine)
    q4=session.query(func.min(Measurement.tobs), func.avg(Measyrement.tobs), func.max(Measurement.tobs))
    session.close()
    return jsonify(q4)
if __name__ == "__main__":
    app.run(debug=True)
  
    