# Author: Aline Jaimes
# Date: 10/02/19
# Name: ClimateApp
# Goal: Design a Flask API based on the climate exploratory analysis.

#1 Import Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# 2 Database Setup
#a. engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = db.create_engine("sqlite:///Resources/hawaii.sqlite")
#b.  reflect an existing database into a new model
Base = automap_base()
# c. reflect the tables
Base.prepare(engine, reflect=True)
# d. Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# 3. Flask Setup
# a. import Flask
from flask import Flask

# b. Create an app, being sure to pass __name__
app = Flask(__name__)


# c. Define what to do when a user hits the index route
@app.route("/")
def Welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )
        
# d. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
    print("Server received request for 'Precipitation' page...")
    return "Here is a list of the last 12 months of precipitation in Hawaii"
    #retrieve the last 12 months of precipitation data
    qr1=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    qr2=dt.date(2017,8,23)-dt.timedelta(days=365)
    ppt=session.query(Measurement.prcp,Measurement.date).\
    filter(Measurement.date > qr2).\
    order_by(Measurement.date).all()

 # e. Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    precipitation=[]
    for result in prcp:
        prcp_dict = {}
        prcp_dict["date"] = prcp[0]
        prcp_dict["prcp"] = prcp[1]
        precipitation.append(prcp_dict)
    
# f. Return the JSON representation of your dictionary.
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'station' page...")
    # Return a JSON list of stations from the dataset.
    return "Here is a list of the stations available"

    stns=session.query(Measurement).group_by(Measurement.station).count()
    print("Hello, there are {} stations available.".format(stns))
    print("Hola, existen {} estaciones disponibles.".format(stns))
    stnsNo=session.query(Measurement.station, func.count(Measurement.station).label('count')).\
    group_by(Measurement.station).all()
    stnsNo_total=[]
    for result1 in stnsNo:
        stnsNo_dict = {}
        stnsNo_dict["date"] = prcp[0]
        stnsNo_dict["prcp"] = prcp[1]
        stnsNo_total.append(stnsNo_dict)
    #Return the JSON representation of your dictionary.
    return jsonify(stnsNo_total)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Precipitation' page...")
    # query for the dates and temperature observations from a year from the last data point.
    return "Here is a list of the last 12 months of air temperature in Hawaii"
    TA=session.query(Measurement.tobs,Measurement.date).\
    filter(Measurement.date > qr2).\
    order_by(Measurement.date).all()

    #Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    AT=[]
    for result in tobs:
        tobs_dict = {}
        tobs_dict["date"] = tobs[0]
        tobs_dict["tobs"] = tobs[1]
        AT.append(tobs_dict)
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(AT)
  
    