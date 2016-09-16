import gmplot
import pandas as pd
import pyowm
import json
import time
from optparse import OptionParser
from geopy.geocoders import Nominatim

parser = OptionParser()
parser.add_option("-a", "--api", dest="api",help="api key to get access to openweather")

(opts, args) = parser.parse_args()
api=opts.api

geolocator = Nominatim()
gmap = gmplot.GoogleMapPlotter(0, 0, 2)
owm = pyowm.OWM(api)
df = pd.read_csv('cities.csv')
df.head()

for index, row in df.iterrows():
  loc_city = str(df.loc[index,"city"]) + "," + str(df.loc[index,"country"])

  iterate = True
  while (iterate):
    try:
        global location,w,observation
        location = geolocator.geocode(df.loc[index,"city"])
        observation = owm.weather_at_coords(location.latitude,location.longitude)
        w = observation.get_weather()
        iterate = False
    except:
        iterate = True

  jsonweather = w.to_JSON()
  jsonloads = json.loads(jsonweather)
  temp = jsonloads["temperature"]["temp"] - 273.15
  text = loc_city + ' Temperature ' + str(temp) + ' Status '  + str(jsonloads['detailed_status'])
  gmap.marker(location.latitude, location.longitude, "blue",title=text)

gmap.draw("index.html")
