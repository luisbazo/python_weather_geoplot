import gmplot
from weather_dicts import icon_weather_codes,mpl_color_map,html_color_codes
import os
import urlparse


class GoogleMapPlotter(gmplot.GoogleMapPlotter):

    pass

    #Redefine init to set up new variables to support weather icon
    def __init__(gmplot, center_lat, center_lng, zoom):
        gmplot.center = (float(center_lat), float(center_lng))
        gmplot.zoom = int(zoom)
        gmplot.grids = None
        gmplot.paths = []
        gmplot.shapes = []
        gmplot.points = []
        gmplot.heatmap_points = []
        gmplot.radpoints = []
        gmplot.gridsetting = None
        gmplot.coloricon = os.path.join(os.path.dirname(__file__), 'markers/%s.png')
        gmplot.color_dict = mpl_color_map
        gmplot.html_color_codes = html_color_codes
        gmplot.icon_weather_codes = icon_weather_codes

    #Redefine marker to support weather icons
    def marker(gmplot,lat, lng, color='#FF0000', c=None, title="no implementation"):
        if c:
            color = c
            #color = gmplot.color_dict.get(color, color)
        color = gmplot.icon_weather_codes.get(color, color)
        gmplot.points.append((lat, lng, color, title))
