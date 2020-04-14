import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

#sql lite path to directory
database_path = "../Resources/hawaii.sqlite"

# Create an engine that can talk to the database
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/precipitation<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of precipitation in hawaii"""
    # Get the last day in the data set
    last_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()

    # Subtract 365 days
    last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # Query all measurement date and precipitation
    measurement_col = (Measurement.date, Measurement.prcp)
    prcp_data = session.query(*measurement_col).\
        filter(Measurement.date >= last_year_date).all()

    session.close()

    # Convert list of tuples into a dictionary 
    di = dict(prcp_data)

    return jsonify(di)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all station names
    station_name = session.query(Station.name).all()

    session.close()

    # Numpy ravel to convert the list withn a list to just a simple list
    station_name = list(np.ravel(station_name))

    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the date and temperature of the most active station of the year"""
    # Query of the temperature of the most active station of the year
    temp = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date > '2016-08-23').all()

    session.close()

    # di = dict(high_num)
    
    # Numpy ravel to convert the list withn a list to just a simple list
    temp = list(np.ravel(temp))

    return jsonify(temp)

if __name__ == '__main__':
    app.run(debug=True)