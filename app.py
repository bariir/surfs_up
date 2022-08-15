# import dependencies datetime, Numpy and Pandas
import datetime as dt
from lib2to3.pytree import Base
from re import M
import numpy as np
import pandas as pd
# import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# import Flask depencies
from flask import Flask, jsonify


# Set up the database engine for the Flask
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()

# Function to reflect our tables
Base.prepare(engine, reflect=True)

# Create variable for each of the classes to reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to our database
session = Session(engine)


# Define our app for our Flask application
app = Flask(__name__)

# Create welcome route
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# Create precipitation route
@app.route("/api/v1.0/precipitation")
# Create precipitation function
def precipitation():
    # Calculate teh date one year ago from the most recent date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    # Use jsonify() function to format the results into JSON structure file.
    # Create a dictionary with the date as a key and precipitation as a value.
    precip = {date: prcp for date, prcp in precipitation}

    # Return precipitation in json format.
    return jsonify(precip)

# Create station route
@app.route("/api/v1.0/stations")
# create station function
def stations():
    # Create a query to get all of the stations in our database.
    results = session.query(Station.station).all()
    # Convert the unraveled results into a list.
    stations = list(np.ravel(results))

    # return station in json format.
    return jsonify(stations=stations)

# Create temperature route
@app.route("/api/v1.0/tobs")
# Create temp_monthly function
def temp_monthly():
    # Calculate the date one year ago from the last date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the primary stations for all the temperature observations from prevous year.
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # Unravel the results into a one-dimensional array and convert into a list.
    temps = list(np.ravel(results))
    
    # return temperature in json format.
    return jsonify(temps=temps)

# Create route for the summary statistics report.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create stats function and add start and end parameters
def stats(start=None, end=None):
    # Create query to select minimum, average, and maximum temperatures from our SQLite database.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
     # Query the database with the list that we just made.
     # Unravel the results into a one-dimensional array and convert them to a list. 
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)