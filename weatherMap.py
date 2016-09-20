import gmplotopenweather as gmplot
import pandas as pd
import pyowm
import json
import time
from optparse import OptionParser
from geopy.geocoders import Nominatim

parser = OptionParser()
parser.add_option("-w", "--apiopenweather", dest="api",help="api key to get access to openweather http://openweathermap.org/appid")
parser.add_option("-m", "--apigooglemaps", dest="apigooglemaps",help="api key to get access to googlemap https://developers.google.com/maps/documentation/javascript/get-api-key")

(opts, args) = parser.parse_args()
api=opts.api
apigooglemaps=opts.apigooglemaps

geolocator = Nominatim()
gmap = gmplot.GoogleMapPlotter(0, 0, 2)
owm = pyowm.OWM(api)
df = pd.read_csv('cities.csv')
df.head()

for index, row in df.iterrows():
  loc_city = str(df.loc[index,"city"]) + "," + str(df.loc[index,"country"])

  iterate = True
  counter = 0
  while (iterate and counter < 5):
    try:
        print "Retrieving information of city " + loc_city
        location = geolocator.geocode(df.loc[index,"city"])
        observation = owm.weather_at_coords(location.latitude,location.longitude)
        w = observation.get_weather()
        jsonweather = w.to_JSON()
        jsonloads = json.loads(jsonweather)
        temp = jsonloads["temperature"]["temp"] - 273.15
        text = loc_city + ' Temperature ' + str(temp) + ' Status '  + str(jsonloads['detailed_status'])
        gmap.marker(location.latitude, location.longitude, str(jsonloads['detailed_status']) ,title=text)
        iterate = False
    except:
        iterate = True
        counter = counter + 1

gmap.draw(apigooglemaps,"index.html")
