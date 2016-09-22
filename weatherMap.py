import gmplotopenweather as gmplot
import pandas as pd
import pyowm
import urllib2,json
import time
from optparse import OptionParser
import sys
#from geopy.geocoders import Nominatim

parser = OptionParser()
parser.add_option("-w", "--apiopenweather", dest="apiopenweather",help="api key to get access to openweather http://openweathermap.org/appid")
parser.add_option("-m", "--apigooglemaps", dest="apigooglemaps",help="api key to get access to googlemap https://developers.google.com/maps/documentation/javascript/get-api-key")

(opts, args) = parser.parse_args()
api=opts.apiopenweather
apigooglemaps=opts.apigooglemaps

#Center defaut map in Europe and zoom 6 times
gmap = gmplot.GoogleMapPlotter(48.51, 2.2, 5)
owm = pyowm.OWM(api)

df = pd.read_csv('cities.csv')
df.head()

for index, row in df.iterrows():
  loc_city = str(df.loc[index,"city"]) + "," + str(df.loc[index,"country"])
  iterate = True
  counter = 0
  while (iterate and counter < 2):
    try:
        print "Retrieving information of city " + loc_city
        #location = geolocator.geocode(df.loc[index,"city"])
        lat,lng = gmap.getCoordinates(df.loc[index,"city"],apigooglemaps)
        #observation = owm.weather_at_coords(location.latitude,location.longitude)
        observation = owm.weather_at_coords(lat,lng)
        w = observation.get_weather()
        jsonweather = w.to_JSON()
        jsonloads = json.loads(jsonweather)

        temp = jsonloads["temperature"]["temp"] - 273.15
        text = '<h1><b>Weather forecast for ' + loc_city + '</b></h1><p></p><p><b>Today</b> ' + str(jsonloads['detailed_status']) + ' ' + str(temp) + ' C'

        fc = owm.daily_forecast_at_coords(lat, lng)
        fcweather = fc.get_forecast()
        jsonfcweather = fcweather.to_JSON()
        jsonfcweatherloads = json.loads(jsonfcweather)

        for s in jsonfcweatherloads['weathers']:
            maxtemp = s['temperature']['max'] - 273.15
            mintemp = s['temperature']['min'] - 273.15
            text = text + '<br>' + '<b>' + time.ctime(int(s['reference_time'])).rsplit(' ', 2)[0] + '</b>' + ' ' + s['detailed_status'] + ' <b>max temp</b> ' + str(maxtemp) + ' C ' + '<b>min temp</b> ' + str(mintemp) + ' C'
        text = text + '</p>'

        gmap.marker(lat, lng, str(jsonloads['detailed_status']) ,title=text)
        iterate = False
    except:
        iterate = True
        counter = counter + 1

gmap.draw(apigooglemaps,"index.html")
