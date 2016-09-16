# python_weather_plotly
This is an example of python program that reads a list of cities from a csv file and it plots temperature data in a map

The project is composed with 3 files

1. weatherMap.py: Python script to get weather data from a list of cities. Once data has been gathered it plots on a google map

  python weatherMap.py -o 1 -a xxxxxxxxxxxxx

  Usage: weatherMap.py [options]

  Options:

                    -h, --help            show this help message and exit
                    -a API, --api=API     api key to get access to openweather

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

  gmplot library could be extended to support more marker icons, labels, formats, etc.
  More weather data could be included in the map. Different kinds of maps and formats could be used.  
  In combination with nosql databases, weather data could be stored and analyzed to be displayed in the map.  
