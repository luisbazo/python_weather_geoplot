#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gmplotopenweather as gmplot
from pymongo import MongoClient
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
writeCSV=False

#Center defaut map in Europe and zoom 6 times
gmap = gmplot.GoogleMapPlotter(40.4167754, -3.7037902, 7)
owm = pyowm.OWM(api)
df = pd.read_csv('country-list-coordinate.csv')
df.head()

for index, row in df.iterrows():
  loc_city = str(df.loc[index,"capital"]) + "," + str(df.loc[index,"country"])
  #If no latitude or longitude then ask google API and write it down to csv at the end of the script
  if(str(df.loc[index,"latitude"]) == "nan" or str(df.loc[index,"longitude"]) == "nan"):
      writeCSV = True
      lat,lng = gmap.getCoordinates(loc_city,apigooglemaps)
      df.loc[index,"latitude"] = lat
      df.loc[index,"longitude"] = lng
  iterate = True
  counter = 0
  while (iterate and counter < 1):
    try:
        print "Retrieving information of city " + loc_city + " latitude: " + str(df.loc[index,"latitude"]) + " longitude: " + str(df.loc[index,"longitude"])
        observation = owm.weather_at_coords(float(df.loc[index,"latitude"]),float(df.loc[index,"longitude"]))
        w = observation.get_weather()
        jsonweather = w.to_JSON()
        jsonloads = json.loads(jsonweather)

        loc_city_html = loc_city.replace("'","")
        loc_city_html = unicode(loc_city_html, 'utf-8')
        loc_city_html = loc_city_html.encode('ascii', 'xmlcharrefreplace')

        temp = jsonloads["temperature"]["temp"] - 273.15

        #Header
        color = gmplot.icon_weather_codes.get(jsonloads['detailed_status'], jsonloads['detailed_status'])
        image = '<img src="markers/%s.png" alt="%s">' % (color,jsonloads['detailed_status'])
        #text = '<h1><b>Weather forecast for ' + loc_city_html + '</b></h1><p></p><p><b>Current</b> ' + str(jsonloads['detailed_status']) + ' ' + str(temp) + ' C'
        #text = '<h1><b>Weather forecast for ' + loc_city_html + '</b></h1><p></p><p><b>Current Status</b> ' + image + ' ' + str(temp) + ' C'
        #text = '<h1><b>' + loc_city_html +  ' ' + str(temp) + ' C' +  ' ' + image + '</b></h1>'
        text = '<h1><b>' + loc_city_html +  ' ' + image + '</b></h1>'

        fc = owm.daily_forecast_at_coords(float(df.loc[index,"latitude"]),float(df.loc[index,"longitude"]))
        fcweather = fc.get_forecast()
        jsonfcweather = fcweather.to_JSON()
        jsonfcweatherloads = json.loads(jsonfcweather)

        #Body table
        text = text + '<table style="width:100%"><tr><th>Date</th><th>Temp Max C</th><th>Temp Min C</th><th>Status</th><th>Rain mm</th><th>Wind km/h</th></tr>'
        for s in jsonfcweatherloads['weathers']:
            #If current time is newer than forecast time then forecast is not forecast anymore continue to next
            if(time.time() > float(s['reference_time'])):
                #print "Skipping old forecast detected for city " + loc_city + " :Current time:" + time.ctime(time.time()) + " forecast time:" + time.ctime(int(s['reference_time']))
                continue

            #Skipping current day forecast
            #if(time.ctime(time.time()).rsplit(' ', 2)[0] == time.ctime(int(s['reference_time'])).rsplit(' ', 2)[0]):
            #    print "Skipping current day forecast detected for city " + loc_city + " :Current time:" + time.ctime(time.time()) + " forecast time:" + time.ctime(int(s['reference_time']))
            #    continue

            maxtemp = s['temperature']['max'] - 273.15
            mintemp = s['temperature']['min'] - 273.15
            windkmh = int((s['wind']['speed']*18)/5)
            color = gmplot.icon_weather_codes.get(s['detailed_status'], s['detailed_status'])
            image = '<img src="markers/%s.png" alt="%s">' % (color,s['detailed_status'])
            text = text + '<tr>' + '<td align="center">' + time.ctime(int(s['reference_time'])).rsplit(' ', 2)[0] + '</td>' + '<td align="center">' + str(maxtemp) + '</td>' + '<td align="center">' + str(mintemp) + '</td>' + '<td align="center">' + image + '</td>' + '<td align="center">' + str(s['rain']['all']) + '</td>' + '<td align="center">' +  str(windkmh) + '</td>' + '</tr>'
        text = text + '</table>'

        gmap.marker(float(df.loc[index,"latitude"]), float(df.loc[index,"longitude"]), str(jsonloads['detailed_status']) ,title=text)
        iterate = False
    except:
        iterate = True
        counter = counter + 1
        time.sleep(0)

if(writeCSV):
    df.to_csv('country-list-coordinate.csv', mode = 'w', index=False, columns=['country','capital','type','latitude','longitude'])

gmap.draw(apigooglemaps,"index.html")
