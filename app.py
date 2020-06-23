# Pablo Fernández R.
import logging.handlers
from logging import FileHandler
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from geoalchemy2 import Geometry
from werkzeug.utils import secure_filename
from werkzeug.debug import DebuggedApplication
import csv
import os.path
from config import Config
import string
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

file_handler = FileHandler('mylog.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

db = SQLAlchemy()
db.init_app(app)

# @app.errorhandler(500)
# def internal_error(exception):
#     app.logger.error(exception)
#     return render_template('500.html'), 500


@app.route("/")
def main_html():
    return render_template("index.html")


@app.route("/api/getall/")
def api_getall():
    querry = """SELECT json_build_object(
    \'geometry\',   ST_AsGeoJSON(geo)::json,
    \'properties\', json_build_object(
	\'PM10.0\', \"PM10_0\",
	\'PM2.5\', \"PM2_5\",
	\'PM1.0\', \"PM1_0\",
	\'NH3\', \"NH3\",
	\'CO\', \"CO\",
	\'NO2\',\"NO2\",
	\'Pressure\', \"Pressure\",
	\'AltBar\', \"AltBar\",
	\'Hum\', \"Hum\",
	\'Temp\', \"Temp\",
	\'AltGPS\', \"AltGPS\",
	\'Long\', \"Longitude\",
	\'Lat\', \"Latitude\",
	\'DateTime\', \"DateTime\"        
     ),
     \'type\',       \'Feature\'
    )  FROM data;"""

    out = "{\"type\":\"FeatureCollection\",\"features\":["

    for q in db.session.execute(querry):
        for d in q:
            out += str(d).replace('\'', '\"')  # .split('(')[1].split(')')[0]
        out += ","
    out = out[:-1]  # remove "," at the end
    out += "]}"
    # db.session
    #a = db.session.query(func.ST_AsGeoJSON(Dataline.query.all())).scalar()
    # db.session.query(func.ST_AsGeoJSON(Dataline.geo)).all()
    #a = jsonify(ast.literal_eval(Dataline.query.first().geo.ST_AsGeoJSON()))
    with open('mylog.log', 'a') as the_file:
        the_file.write('access  {}\n'.format(datetime.now()))
        # pass
    for d in db.session.execute(querry):
        pass  # db.alll()

    # str(db.session.query(func.ST_AsGeoJSON(Dataline.geo)).first()).split('\'')[1] # "{\"type\":\"Feature\",\"geometry\":"+(str(db.session.query(func.ST_AsGeoJSON(Dataline.geo)).first()).split('\'')[1])+"}"
    return out
# out # (type(req['n']))
# https://stackoverflow.com/questions/23740548/how-do-i-pass-variables-and-data-from-php-to-javascript
# https://stackoverflow.com/questions/1873083/in-postgis-how-do-i-find-all-points-within-a-polygon
    # https://postgis.net/workshops/postgis-intro/spatial_relationships.html#st-within-and-st-contains


# https://ipfs-sec.stackexchange.cloudflare-ipfs.com/gis/A/question/16374.html
@app.route("/api/get/")
def api_get():  # TODO only numbers can be pass
    querry = """SELECT json_build_object(
    \'geometry\',   ST_AsGeoJSON(geo)::json,
    \'properties\', json_build_object(
	\'PM10.0\', \"PM10_0\",
	\'PM2.5\', \"PM2_5\",
	\'PM1.0\', \"PM1_0\",
	\'NH3\', \"NH3\",
	\'CO\', \"CO\",
	\'NO2\',\"NO2\",
	\'Pressure\', \"Pressure\",
	\'AltBar\', \"AltBar\",
	\'Hum\', \"Hum\",
	\'Temp\', \"Temp\",
	\'AltGPS\', \"AltGPS\",
	\'Long\', \"Longitude\",
	\'Lat\', \"Latitude\",
	\'DateTime\', \"DateTime\"        
     ),
     \'type\',       \'Feature\'
    )  FROM data;"""

    out = "{\"type\":\"FeatureCollection\",\"features\":["

    for q in db.session.execute(querry):
        for d in q:
            out += str(d).replace('\'', '\"')  # .split('(')[1].split(')')[0]
        out += ","
    out = out[:-1]  # remove "," at the end
    out += "]}"
    # db.session
    #a = db.session.query(func.ST_AsGeoJSON(Dataline.query.all())).scalar()
    # db.session.query(func.ST_AsGeoJSON(Dataline.geo)).all()
    #a = jsonify(ast.literal_eval(Dataline.query.first().geo.ST_AsGeoJSON()))
    with open('mylog.log', 'a') as the_file:
        the_file.write('access  {}\n'.format(datetime.now()))
        # pass
    for d in db.session.execute(querry):
        pass  # db.alll()

    return out


@app.route("/api/send/")
def api_send():
    # print(Dataline.add_dataline("7/7/19","17:57:50",40.4103952,-3.693736+0.00001*int(request.args.get('n')),0,26.58,32,618.9,941.09,34.99,2.97,0,0,0,2))
    n = request.args.get('n')
    # (type(req['n']))
    return str(-3.693736+0.00001*int(request.args.get('n')))+'\n'
# https://postgis.net/workshops/postgis-intro/indexing.html#analyzing  #update its internal statistics
# https://postgis.net/workshops/postgis-intro/indexing.html#vacuuming


@app.route('/getfile', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':

        # for secure filenames. Read the documentation.
        file = request.files['myfile']
        filename = secure_filename(file.filename)

        # os.path.join is used so that paths work in every operating system
        # file.save(os.path.join("temp",filename))
        file.save(os.path.join("/data/www/temp", filename))

        with open(os.path.join("/data/www/temp", filename)) as f:
            csvreader = csv.reader(f, delimiter=',')
            next(csvreader)  # first line contains labels
            next(csvreader)  # second line is empty
            # 0     1    2       3     4   5        6        7    8   9    10      11    12       13   14
            # .csv = Lat, Long, AltGPS, Temp, Hum, AltBar, Pressure, NO2, CO, NH3, PM1.0, PM2.5, PM10.0 ,Date, Time
            #add_dataline = cls, Date, Time, Latitude, Longitude, AltGPS, Temp, Hum, AltBar, Pressure, NO2, CO, NH3, PM1_0, PM2_5, PM10_0
            for row in csvreader:  # TODO adapt to NOTO .csv form
                Dataline.add_dataline(row[13], row[14], row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                      row[7], row[8], row[9], row[10], row[11], row[12])
                # Dataline.add_dataline(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                #                       row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
            f.close()
            os.remove(os.path.join("/data/www/temp", filename))

        return redirect('/')
    else:
        result = request.args.get['myfile']
        result += "ERROROROR"
    return result

# borrows heavily from the wonderlful tutorial from jgriffith23: https://github.com/jgriffith23/postgis-tutorial


class Dataline(db.Model):
    """A datapoint collection aka dataline with Date & Timestamp"""

    __tablename__ = "data"

    point_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DateTime = db.Column(db.DateTime)
    geo = db.Column(Geometry(geometry_type="POINT"))
    Latitude = db.Column(db.Float, default=0.0)
    Longitude = db.Column(db.Float, default=0.0)
    AltGPS = db.Column(db.Float, default=0.0)
    Temp = db.Column(db.Float, default=0.0)
    Hum = db.Column(db.Float, default=0.0)
    AltBar = db.Column(db.Float, default=0.0)
    Pressure = db.Column(db.Float, default=0.0)
    NO2 = db.Column(db.Float, default=0.0)
    CO = db.Column(db.Float, default=0.0)
    NH3 = db.Column(db.Float, default=0.0)
    PM1_0 = db.Column(db.Float, default=0.0)
    PM2_5 = db.Column(db.Float, default=0.0)
    PM10_0 = db.Column(db.Float, default=0.0)

    # def __repr__(self):
    #     return "<dataLINE  {Latitude}, {Longitude}, {AltGPS}, {Temp}, {Hum}, {AltBar}, {Pressure}, {NO2}, {CO}, {NH3}, {PM1_0}, {PM2_5}, {PM10_0} ,{DateTime})>".format(Latitude=self.Latitude, Longitude=self.Longitude, AltGPS=self.AltGPS, Temp=self.Temp, Hum=self.Hum, AltBar=self.AltBar, Pressure=self.Pressure, NO2=self.NO2, CO=self.CO, NH3=self.NH3, PM1_0=self.PM1_0, PM2_5=self.PM2_5, PM10_0=self.PM10_0, DateTime=self.DateTime)

    # def get_cities_within_radius(self, radius):
    #     """Return all cities within a given radius (in meters) of this city."""

    #     return City.query.filter(func.ST_Distance_Sphere(City.geo, self.geo) < radius).all()

    @classmethod
    def add_dataline(cls, Date, Time, Latitude, Longitude, AltGPS, Temp, Hum, AltBar, Pressure, NO2, CO, NH3, PM1_0, PM2_5, PM10_0):
        """Put a new dataline in the database."""
        # TODO DateTime
        db.session.add(Dataline(DateTime=datetime.now(), geo='POINT({} {})'.format(Longitude, Latitude), Latitude=Latitude, Longitude=Longitude,
                                AltGPS=AltGPS, Temp=Temp, Hum=Hum, AltBar=AltBar, Pressure=Pressure, NO2=NO2, CO=CO, NH3=NH3, PM1_0=PM1_0, PM2_5=PM2_5, PM10_0=PM10_0))
        db.session.commit()


with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    print("drfgklhjñḱ")
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
