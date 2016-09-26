# python_weather_plotly

This is an example of python program that reads a list of cities from a csv file and it plots weather data retrieved from Open Weather Site (https://openweathermap.org) in a google map including a 7-day forecast for each of the cities. The html containing the map can be published in a web server (Ex. Apache Web Server) to be accessed externally. The program receives two parameters. One key API to get access to open weather data and another key API to get access to google maps. Both keys could be obtained for free. Look at the python program help to get information of how to obtain API keys needed to run the program.

Library gmplot has been extended,
  -It has been added support to weather icons from open weather
  -It has been added the google API key on map draw which has been recently declared mandatory by Google to generate the map if the map is served from a public web domain.

You can see a map example generated on https://luisbazo.github.io/python_weather_geoplot/. Data is refreshed automatically every 4 hours.

The project is composed with 3 files

1. weatherMap.py: Python script to get weather data from a list of cities. Once data has been gathered it plots on a google map

Usage: weatherMap.py [options]

Options:
    -h, --help            show this help message and exit

    -w APIOPENWEATHER, --apiopenweather=API
                      api key to get access to openweather http://openweathermap.org/appid

    -m APIGOOGLEMAPS, --apigooglemaps=APIGOOGLEMAPS
                      api key to get access to googlemap https://developers.google.com/maps/documentation/javascript/get-api-key

Once executed the map is automatically generated in a file called index.html under the script folder.

2. cities.csv: CSV file with the list of cities to retrieve weather data from

Example:

iata,airport,city,state,country,lat,long,temp
null,Madrid SP,Madrid,SP,SP,null,null,null
null,London Uk,London,UK,UK,null,null,null

Some of the columns are not used but they could be used in future script versions

3. index.html: THe result HTML google map file with cities weather

Prerequisites

  Python Libraries


  Use library pyown to get weather data from http://openweathermap.org/. To install execute command

      pip install pyowm


  Use library geopy to get cities coordinates https://github.com/geopy/geopy

      pip install geopy

  Use library gmplot to print out map https://github.com/vgm64/gmplot

      pip install gmplot    

  Extensions

  gmplot library could be extended to support improved icons, labels, formats, etc.
  More weather data could be included in the map. Different kinds of maps and formats could be used.  
  In combination with nosql databases, weather data could be stored and analyzed to be displayed in the map.  
