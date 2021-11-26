import folium
import pandas

map = folium.Map(location=[45, -100], zoom_start=6, tiles="Stamen Terrain")

html = """
Volcano name: <br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_elev(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <= 3000:
        return 'orange'
    else:
        return 'red'


feature_p = folium.FeatureGroup(name="Population")
feature_p.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

feature_v = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name,name, el), width=200, height=100)
    feature_v.add_child(folium.CircleMarker(location=[lt, ln], color='black', radius=6,popup=folium.Popup(iframe), fill_color=color_elev(el), fill_opacity=0.7))

map.add_child(feature_v)
map.add_child(feature_p)
map.add_child(folium.LayerControl())
map.save("Map1.html")