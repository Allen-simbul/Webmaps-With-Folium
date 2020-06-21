import pandas
import folium

data = pandas.read_csv("volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
name = list(data["NAME"])
location = list(data["LOCATION"])
status = list(data["STATUS"])
volcanic_type = list(data["TYPE"])
elev = list(data["ELEV"])


def color_producer(elevation):
    if (elevation < 1000):
        return 'green'
    elif (1000 <= elevation < 3000):
        return 'orange'
    else:
        return 'red'


html = """
<div>
    <h4>Volcano information:</h4>
    <p>Name: %s</p>
    <p>Location: %s</p>
    <p>Status: %s</p>
    <p>Type: %s</p>
    <p>Elevation: %s m</p>
</div>
"""

map = folium.Map(location=[38.58, -99.09],
                 zoom_start=6, tiles="Stamen Toner")

# Shows Data on Volcanoes in United States
fgv = folium.FeatureGroup(name="My Map")

for lt, ln, nm, loc, stat, vc_type, el in zip(lat, lon, name, location, status, volcanic_type, elev):
    iframe = folium.IFrame(html=html % (
        nm, loc, stat, vc_type, str(el)), width=220, height=220)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(
        iframe), fill_color=color_producer(el), color="grey", fill=True, fill_opacity=0.7))

# Shows Population of Country based on color
fgp = folium.FeatureGroup(name='Population')

fgp.add_child(folium.GeoJson(
    data=open('world.json', 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {
        'fillColor': 'green'
        if x['properties']['POP2005'] < 10000000 else 'orange'
        if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}
))

map.add_child(fgv)
map.add_child(fgp)
# Adds Layer Control Panel to Folium Map
map.add_child(folium.LayerControl())

map.save("Map1.html")
