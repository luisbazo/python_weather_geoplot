import gmplotopenweather as gmplot
from pymongo import MongoClient
import pandas as pd
import pyowm
import urllib2,json
import time
from optparse import OptionParser
import sys


parser = OptionParser()
#parser.add_option("-w", "--apiopenweather", dest="apiopenweather",help="api key to get access to openweather http://openweathermap.org/appid")
parser.add_option("-m", "--apigooglemaps", dest="apigooglemaps",help="api key to get access to googlemap https://developers.google.com/maps/documentation/javascript/get-api-key")

(opts, args) = parser.parse_args()
apigooglemaps=opts.apigooglemaps


df = pd.read_csv('country-list.csv')
df.head()

gmap = gmplot.GoogleMapPlotter(48.51, 2.2, 5)

for index, row in df.iterrows():
  loc_city = str(df.loc[index,"capital"]) + "," + str(df.loc[index,"country"])
  lat,lng = gmap.getCoordinates(loc_city,apigooglemaps)
  df.loc[index,"latitude"] = lat
  df.loc[index,"longitude"] = lng

df.to_csv('country-list-coordinate.csv')
