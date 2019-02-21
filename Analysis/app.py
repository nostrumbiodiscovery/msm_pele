# coding: utf-8

from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import Query.query as qr
import json

app = Flask(__name__, template_folder="templates")
MADRID_LAT = 40.4167
MADRID_LNG = -3.70325
#Have to add new feature for open
COMP_FIELDS = ["CON_SALDO", 1]

@app.route("/")
def index(lat=MADRID_LAT, lng=MADRID_LNG, filtering=None):
    return render_template('index.html', lat=lat,lng=lng, locations=retrieve_atms_location(qr.cajeros_df, filtering))

def retrieve_atms_location(atms, filtering=None):
    # filtering: list such as: [[tranfer, 1], [conctless,1]]
    if filtering:

        conditions = True
        for crit, value in filtering:
            conditions &= (qr.cajeros_df[crit] == value)            
        df = qr.cajeros_df[conditions]

    else:
        df = qr.cajeros_df

    return df[['NOMBRE_CALLE', 'latitud', 'longitud']].values.tolist()
    

@app.route('/filter', methods = ['POST', 'GET'])
def filter():
    print("AAA")
    if request.method == 'POST':
        user_action = request.form["user_action"]
        return index([[user_action, 1], COMP_FIELDS])
    else:
        return render_template('index.html', lat=MADRID_LAT, lng=MADRID_LNG)
    
@app.route('/closest_atm', methods = ['POST', 'GET'])
def closest_atm():
    if request.method == 'POST':
        #Later from DB
        atms = qr.cajeros_df[['latitud', 'longitud']]
        #Initialize object
        query = qr.Query("a", "b", "driving")
        #make query
        user_location = qr.gmaps.geocode(request.form["position"])[0]['geometry']['location']
        atm = query.closest_point_to(atms, user_location, lat_v="lat", lng_v="lng")
        return render_template('index.html', lat=atm["latitud"], lng=atm["longitud"])
    else:
        return render_template('index.html', lat=MADRID_LAT, lng=MADRID_LNG)




@app.route('/clickpost/', methods=['POST'])
def clickpost():
    # Now lat and lon can be accessed as:
    lat = request.form['lat']
    lng = request.form['lng']
    print(lat)
    print(lng)
    return "ok"



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

