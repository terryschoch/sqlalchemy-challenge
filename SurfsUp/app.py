# Import Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
        f"Welcome to Surf's Up Weather Alchemy!<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query date and precipitation values for past year only    
    prevyear_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23").\
    order_by(Measurement.date).all()

    session.close()

    # Convert queried list of tuples into dictionary with date as key and prcp as value
    prevyear_precipitation = dict((x, y) for x, y in prevyear_prcp)    

    return jsonify(prevyear_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    station_data = session.query(Station.name).all()

    session.close()

  # Convert queried list of tuples into normal list
    all_stations = list(np.ravel(station_data))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return tobs data for only the past year of the most active station"""
    # Query only the most active station most recent year's worth of results
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= "2016-08-23").all()

    session.close()

  # Convert queried list of tuples into dictionary with date as key and tobs as value
    most_active_station = dict((x, y) for x, y in tobs_data)    
    # most_active_station = list(np.ravel(results))

    return jsonify(most_active_station)


@app.route("/api/v1.0/<start>")
def start_temps(start):
    """Fetch the Min, Avg, and Max Temperatures for the range beginning from the date 
    variable supplied by the user, or a 404 if not."""
     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for avg, min & max temps    
    defsel = [func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)]
    
    start_range = session.query(*defsel).\
        filter(Measurement.date >= start).all()
    
    session.close()

  # Convert queried list of tuples into normal list
    start_results = list(np.ravel(start_range))

    return jsonify(start_results)       


@app.route("/api/v1.0/<start>/<end>")
def start_end_temps(start, end):
    """Fetch the Min, Avg, and Max Temperatures for the range beginning from the start date 
    to the end date variables supplied by the user, or a 404 if not."""
     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for avg, min & max temps    
    defsel = [func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)]
    
    start_end_range = session.query(*defsel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()

  # Convert queried list of tuples into normal list
    start_end_results = list(np.ravel(start_end_range))

    return jsonify(start_end_results)  

if __name__ == '__main__':
    app.run(debug=True)