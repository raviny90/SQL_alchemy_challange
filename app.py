import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
from flask import render_template

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station 

# Flask Setup
app = Flask(__name__)

# Flask Routes
climate_app_art = "https://moesucks.files.wordpress.com/2018/08/persona-5-the-animation-18-14.jpg"

station_app = "http://127.0.0.1:5000/api/v1.0/stations"

precipitation_app = "http://127.0.0.1:5000/api/v1.0/precipitation"

tobs_app = "http://127.0.0.1:5000/api/v1.0/tobs"

specific_app = "http://127.0.0.1:5000/api/v1.0/2017-01-01"

range_app = "http://127.0.0.1:5000/api/v1.0/2016-01-01/2017-01-01"

@app.route("/")
def home():
    return (
        f"<h1><center>Hawaii 'Climate App'</h1></center><br>"
        f"<center><img src={climate_app_art}></center><br>"
        f"<b><center><h2>Available App Routes :: [Raw Data Sets]</b></h2></center><br>"
        f"<h2><center><a href={precipitation_app}>Hawaii [Precipitation] App</a></h2></center><br>"
        f"<h2><center><a href={station_app}>Hawaii [Stations] App</a></h2></center><br>"
        f"<h2><center><a href={tobs_app}>Hawaii [Observed Temperatures] App</a></h2></center><br>"
        f"<b><center><h2>Available App Routes :: [Min, Avg, Max Temperatures]</b></h2></center><br>"
        f"<h2><center><a href={specific_app}>Hawaii Observed Temperatures [Specific Date] App</a></h2></center><br>"
        f"<h2><center><a href={range_app}>Hawaii Observed Temperatures [Specific Range] App</h2></center>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    precipitation_list = []
    
    for x in results:
        list_dict = {}
        list_dict['Date'] = x.date
        list_dict['Rainfall Amount'] = x.prcp
        precipitation_list.append(list_dict)
    
        session.close()
        
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    all_stations = []
    for x in results:
        list_dict = {}
        list_dict['Station No.'] = x.station
        list_dict['Station Location'] = x.name
        list_dict['Latitude'] = x.latitude
        list_dict['Longitude'] = x.longitude
        list_dict['Elevation'] = x.elevation
        all_stations.append(list_dict)
    
    
        session.close()

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    results = session.query(Measurement.station, Station.name, Measurement.date, Measurement.tobs).\
                            filter(Measurement.station == Station.station).\
                            filter(Measurement.date >= '2016-08-24').\
                            filter(Measurement.date <= '2017-08-24').\
                            order_by(Measurement.date).all()
     
    tobs_list = []
    for x in results:
        list_dict = {}
        list_dict['Name'] = x.name
        list_dict['Date'] = x.date
        list_dict['Temp_Observed'] = x.tobs
        tobs_list.append(list_dict)

    
        session.close()

    return jsonify(tobs_list)


@app.route("/api/v1.0/<date>")
def temperatures_date(date):

    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= date ).all()
    
    temperatures = []
    for x in results:
        list_dict = {}
        list_dict['min'] = results[0][0]
        list_dict['avg'] = round(results[0][1],2)
        list_dict['max'] = results[0][2]
        temperatures.append(list_dict)


        session.close()
    return(    
        f"<center><h3>Temperature Stats For {date}:</h3></center><br>"    
        f"<center>The Min Temperature Was {list_dict['min']} Degrees.</center><br>"
        f"<center>The Average Temperature Was {list_dict['avg']} Degrees.</center><br>"
        f"<center>The Max Temperature Was {list_dict['max']} Degrees.</center>"
    )


@app.route("/api/v1.0/<start>/<end>")
def temperatures_start(start, end):

    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start ).\
                filter(Measurement.date <= end ).all()

    temperatures = []
    for x in results:
        list_dict = {}
        list_dict['min'] = results[0][0]
        list_dict['avg'] = round(results[0][1],2)
        list_dict['max'] = results[0][2]
        temperatures.append(list_dict)


        session.close()

    return(   
        f"<center><h3>Temperature Stats Between {start} And {end}:</h3></center><br>"    
        f"<center>The Min Temperature Was {list_dict['min']} Degrees.</center><br>"
        f"<center>The Average Temperature Was {list_dict['avg']} Degrees.</center><br>"
        f"<center>The Max Temperature Was {list_dict['max']} Degrees.</center>"
    )


# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)