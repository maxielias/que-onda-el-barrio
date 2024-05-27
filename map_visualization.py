import folium
from folium.plugins import MarkerCluster
import json


with open('loc_coord.json', 'r') as file:
    location = json.load(file)

# Create a map centered around the provided coordinates
map_center = location['location'].split(',') # [float(c) for c in location['location'].split(',')]
mymap = folium.Map(location=map_center, zoom_start=15)

# Add markers for each place
marker_cluster = MarkerCluster().add_to(mymap)

with open('places_info.json', 'r') as file:
    places_info = json.load(file)

for place in places_info:
    folium.Marker(
        location=[place['latitude'], place['longitude']],
        popup=f"{place['name']}<br>Rating: {place.get('rating', 'N/A')}<br>{place['vicinity']}",
        icon=folium.Icon(color='blue' if place['opening_hours'] else 'red')
    ).add_to(marker_cluster)

# Save the map as an HTML file
mymap.save('places_map.html')

# Display map inline (for Jupyter notebooks)
#mymap

# Visualization with Matplotlib
import matplotlib.pyplot as plt

# Extract ratings for visualization
ratings = [place['rating'] for place in places_info if place['rating'] is not None]
names = [place['name'] for place in places_info if place['rating'] is not None]

plt.figure(figsize=(10, 6))
plt.barh(names, ratings, color='skyblue')
plt.xlabel('Rating')
plt.ylabel('Place')
plt.title('Ratings of Places in the Area')
plt.tight_layout()
plt.savefig('ratings_bar_chart.png')
plt.show()
