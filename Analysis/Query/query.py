import googlemaps
from math import *
import os
import pandas as pd
from datetime import datetime
import gmplot

DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

cajeros_df = pd.read_csv(
    #os.path.join(DIR, 'cajamar_datathon/files/Cajeros.txt')
    'files/Cajeros.txt'
    , header = 0
    , dtype = str
    , sep = '|'
    , encoding = 'latin-1'
)
cajeros_df.latitud = pd.to_numeric(cajeros_df.latitud)
cajeros_df.longitud = pd.to_numeric(cajeros_df.longitud)

#with open(os.path.join(DIR, 'cajamar_datathon/files/apikey.txt')) as f:
with open('files/apikey.txt') as f:
    api_key = f.readline().strip("\n").strip()
    f.close
    
import gmaps
gmaps.configure(api_key=api_key)

gmaps = googlemaps.Client(key=api_key)
location_1 = (cajeros_df.latitud.values[0], cajeros_df.longitud.values[0])
location_2 = (cajeros_df.latitud.values[1], cajeros_df.longitud.values[1])


class Query(object):
    """
    Base class to make distance&instructions between 2 points
    or find the closest point ginven some data and a query vector
    """
    #modes can be "driving", "walking", "transit" or "bicycling".
    def __init__(self, location1, location2, mode):
        self.location1 = location_1
        self.location2 = location_2
        self.mode = mode
    
    def distance(self):
        self.query_distance = gmaps.distance_matrix(self.location1, self.location2, mode=self.mode)
        self.time = self.query_distance["rows"][0]["elements"][0]["duration"]["text"]
        self.distance_to_origin = self.query_distance["rows"][0]["elements"][0]["distance"]["text"]
        self.origin = self.query_distance['origin_addresses'][0]
        self.destination = self.query_distance['destination_addresses'][0]
        
    def directions(self):
            self.query_direction = gmaps.directions(self.location1, self.location2, mode="driving", alternatives=False)
            instructions  = self.query_direction[0]["legs"][0]["steps"]
            
            #Done to save time (just traverse the list 1 time)
            self.origin_lat, self.origin_long = instructions[0].get("start_location").values()
            self.latitudes = []
            self.longitudes = []
            self.instructions = []
            for instruct in instructions:
                
                final_point = instruct.get("end_location")
                self.latitudes.append(float(final_point["lat"]))
                self.longitudes.append(float(final_point["lng"]))
                self.instructions.append(instruct.get('html_instructions'))

    def closest_point_to(self, data, location, lat_v="latitud", lng_v="longitud", lat_data="latitud", lng_data="longitud"):
        """
        data: pandas dataframe with column of latitud and longitud
        location: dict like {"latitud":41.122145, "longitud":-0.350494}
        you can change the keys va settint lat and lng arguments
        """
        data = data.to_dict(orient="records")
        self.closest_to = location
        self.closest =  min(data, key=lambda p: self.__distance__(self.closest_to[lat_v], self.closest_to[lng_v], p[lat_data], p[lng_data]))
        self.closest_dist = self.__distance__(self.closest_to[lat_v], self.closest_to[lng_v],
                                     self.closest[lat_data], self.closest[lng_data])
        #Get read of it on production
        self.closest_units = "km"
        return self.closest
        
    @staticmethod
    def __distance__(lat1, lon1, lat2, lon2):
        #https://en.wikipedia.org/wiki/Haversine_formula
        #results in km
        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(a))
                
    def plot(self):
        try:
            gmap3 = gmplot.GoogleMapPlotter(query.origin_lat, query.origin_long, 13, apikey=api_key)  
            gmap3.plot(query.latitudes, query.longitudes,  'blue',  edge_width=1) 
            gmap3.draw("hola.html")
            
        except AttributeError:
            self.directions()
            self.plot()
if __name__ == "__main__":        
    import time
    time1 = time.time()
    location_1 = (cajeros_df.latitud.values[0], cajeros_df.longitud.values[0])
    location_2 = (cajeros_df.latitud.values[1], cajeros_df.longitud.values[1])
    locations = cajeros_df[['latitud', 'longitud']]
    query = Query(location_1, location_2, "driving")
    for i in range(100):                
        v = {"latitud":41.832145, "longitud":-0.350494}
        query.distance()
        query.directions()
        query.plot()
        query.closest_point_to(locations, v)
        print(query.closest, query.closest_to, query.closest_dist)
    time2 = time.time()

    #slow pass to cython and parallelize!!!! 
    #13.6s 100 querys of closest
    #35.118 s 100 queries to create plot etc (google maps pretty fast)
    print('function took %0.3f s' % ((time2-time1)))
