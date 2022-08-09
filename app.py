#dependencies
from flask import Flask, jsonify
import datetime as dt
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#connect and reflect data from hawaii.sqlite
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)

# assign sql tables to classes
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br>
    Available Routes: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()
    
    stations = list(np.ravel(results))
    
    return jsonify(stations=stations) 

@app.route("/api/v1.0/tobs")
def temp_monthly():
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter((Measurement.station == 'USC00519281') & (Measurement.date >= prev_year)).all()
    
    temps = list(np.ravel(results))

    return jsonify(temps = temps)


@app.route("/api/v1.0/temp/<start>")

@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start = None, end = None):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs), 2), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        temps = list(np.ravel(results))

        return jsonify(temps)
    
    results = session.query(*sel).\
        filter((Measurement.date >= start) & (Measurement.date <= end)).all()
    
    temps = list(np.ravel(results))

    return jsonify(temps)
