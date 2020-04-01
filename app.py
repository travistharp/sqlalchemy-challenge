#import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

#################################################

#Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Request received for Home page")
    return (
        f"Hawaii Climate Analysis Home Page<br/>"
        f"Available Routes:<br/>"
        f"--------------------------"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"---------------------------"  
    )

# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = '2017-08-23'
    prev_year = '2016-08-23'

   # Perform a query to retrieve the data and precipitation scores
    prcp = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= prev_year).filter(Measurement.date <= last_date).all()

    session.close()

    precip_dict = dict(prcp)

    return jsonify(precip_dict)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()
    station_list = list(np.ravel(stations))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = '2017-08-23'
    prev_year = '2016-08-23'
    station = 'USC00519281'
    temps = session.query(Measurement.date,Measurement.tobs).filter_by(station = station).\
    filter(Measurement.date >= prev_year).filter(Measurement.date <= last_date).all()
    session.close()
    temps = list(np.ravel(temps))
  
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def cal_temp(start=None,end=None):
    session = Session(engine)
    if not end:
        result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    else:
        result= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)