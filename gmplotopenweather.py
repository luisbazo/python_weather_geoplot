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
        #gmplot.coloricon = os.path.join(os.path.dirname(__file__), 'markers/%s.png')
        gmplot.coloricon = 'markers/%s.png'
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

    def draw(gmplot, api, htmlfile):
        f = open(htmlfile, 'w')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write(
            '<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
        f.write(
            '<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
        f.write('<title>Google Maps - pygmaps </title>\n')
        f.write('<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?api=%s&libraries=visualization&sensor=true_or_false"></script>\n' % api)
        f.write('<script type="text/javascript">\n')
        f.write('\tfunction initialize() {\n')
        gmplot.write_map(f)
        gmplot.write_grids(f)
        gmplot.write_points(f)
        gmplot.write_paths(f)
        gmplot.write_shapes(f)
        gmplot.write_heatmap(f)
        f.write('\t}\n')
        f.write('</script>\n')
        f.write('</head>\n')
        f.write(
            '<body style="margin:0px; padding:0px;" onload="initialize()">\n')
        f.write(
            '\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
        f.write('</body>\n')
        f.write('</html>\n')
        f.close()
