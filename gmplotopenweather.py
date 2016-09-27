import gmplot
from weather_dicts import icon_weather_codes,mpl_color_map,html_color_codes
import os
import urlparse
import urllib2,json


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
        f.write('<title>The Weather Map - luis.bazo@gmail.com </title>\n')
        f.write('<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=%s&libraries=visualization&sensor=true_or_false"></script>\n' % api)
        f.write('<script type="text/javascript">\n')
        f.write('\tfunction initialize() {\n')
        gmplot.write_map(f)
        gmplot.write_location(f)
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

    def write_location(gmplot,f):
        f.write('\t\tvar infoWindow = new google.maps.InfoWindow({map: map});\n')
        f.write('\t\tif (navigator.geolocation) {\n')
        f.write('\t\t\tnavigator.geolocation.getCurrentPosition(function(position) {\n')
        f.write('\t\t\tvar pos = {\n')
        f.write('\t\t\t\tlat: position.coords.latitude,\n')
        f.write('\t\t\t\tlng: position.coords.longitude,\n')
        f.write('\t\t\t};\n')
        f.write('\t\t\tinfoWindow.setPosition(pos);\n')
        f.write('\t\t\tinfoWindow.setContent(\'Your location.\');\n')
        f.write('\t\t\tmap.setCenter(pos);\n')
        f.write('\t\t\t});\n')
        f.write('\t\t}\n')

    def write_points(geoplot, f):
        for point in geoplot.points:
            geoplot.write_point(f, point[0], point[1], point[2], point[3])

    def write_point(geoplot, f, lat, lon, color, title):
        f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n' %
            (lat, lon))
        f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' %
            (geoplot.coloricon % color))
        f.write('\t\tvar marker = new google.maps.Marker({\n')
        #f.write('\t\ttitle: "%s",\n' % title)
        f.write('\t\ticon: img,\n')
        f.write('\t\tposition: latlng\n')
        f.write('\t\t});\n')
        f.write('\t\tmarker.setMap(map);\n')
        f.write('\n')

        f.write('\t\tmarker.addListener(\'click\', function() {\n')
        f.write('\t\tvar infoWindow = new google.maps.InfoWindow({map: map});\n')
        f.write('\t\tinfoWindow.setContent(\'%s\');\n' % title)
        f.write('\t\tinfoWindow.setPosition(latlng);\n')
        f.write('\t\tinfoWindow.open(map, this);\n')
        f.write('\t\t});\n');
        f.write('\n')

    def getCoordinates(gmplot,address,apigooglemaps):
        address = address.replace (" ", "+")
        response = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address,apigooglemaps))
        data = json.loads(response.read())
        lat = 0
        lng = 0
        for s in data['results']:
            lat = s['geometry']['location']['lat']
            lng = s['geometry']['location']['lng']
            #In the remote case there are multiple geometry results offered for same city,country combination -> pick up first and break loop
            break
        return [lat,lng]
