# Import the dependencies.

import warnings
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# all API routes available

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        "Available Routes:<br/>"
        "<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        "<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        "<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        "<a href='/api/v1.0/start'>/api/v1.0/start</a><br/>"
        "<a href='/api/v1.0/start/end'>/api/v1.0/start/end</a><br/>"
    )

# API route that shows precipitation for every day for the most recent year

@app.route("/api/v1.0/precipitation")
def get_precipitation():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    precipitation_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    
    session.close()

    precipitation_dict = {date: prcp for date, prcp in precipitation_query}

    return jsonify(precipitation_dict)

# API route that shows a dictionary of all the stations in the table

@app.route("/api/v1.0/stations")
def get_stations():

    stations_query = session.query(Measurement.station).\
        group_by(Measurement.station).all()

    station_dict = [{'station': station[0]} for station in stations_query]

    session.close()

    return jsonify(station_dict)

# API route that shows most recent year's temperature for station: USC00519281

@app.route("/api/v1.0/tobs")
def get_tobs():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_query = session.query(Measurement.tobs, Measurement.date).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= prev_year).all()

    session.close()

    tobs_dict = {date: tobs for tobs, date in tobs_query}

    return jsonify(tobs_dict)

# API route that shows most min temperature, the avg temperature, and the max temperature of Hawaii starting in 2015 to most recent date

@app.route("/api/v1.0/start")
def get_start():

    temp_min_max_avg_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= '2015-01-01').all()
    
    session.close()

    temp_min_max_avg_dict = {'min': temp_min_max_avg_query[0][0], 'avg': temp_min_max_avg_query[0][1], 'max': temp_min_max_avg_query[0][2]}

    return jsonify(temp_min_max_avg_dict)

# API route that shows most min temperature, the avg temperature, and the max temperature of the most recent year

@app.route("/api/v1.0/start/end")
def get_start_end():
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    recent_year_min_max_avg_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                                filter(Measurement.date >= prev_year).all()

    session.close()

    recent_year_min_max_avg_dict = {'min': recent_year_min_max_avg_query[0][0], 'avg': recent_year_min_max_avg_query[0][1], 'max': recent_year_min_max_avg_query[0][2]}

    return jsonify(recent_year_min_max_avg_dict)

if __name__ == '__main__':
    app.run(debug=True)
