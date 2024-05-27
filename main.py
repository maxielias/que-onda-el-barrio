import json
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt

# Load the JSON data from the file
with open('nearby_places.json', 'r') as file:
    data = json.load(file)

# Extract relevant information
places_info = []

for place in data['results']:
    place_info = {
        'name': place.get('name'),
        'latitude': place['geometry']['location']['lat'],
        'longitude': place['geometry']['location']['lng'],
        'vicinity': place.get('vicinity'),
        'rating': place.get('rating'),
        'user_ratings_total': place.get('user_ratings_total'),
        'types': place.get('types'),
        'business_status': place.get('business_status'),
        'opening_hours': place.get('opening_hours', {}).get('open_now'),
        'photos': place.get('photos', []),
    }
    places_info.append(place_info)

# Generate textual report
def generate_report(places_info):
    report = []
    for place in places_info:
        report.append(f"Name: {place['name']}")
        report.append(f"Location: {place['latitude']}, {place['longitude']}")
        report.append(f"Vicinity: {place['vicinity']}")
        report.append(f"Rating: {place.get('rating', 'N/A')} (based on {place.get('user_ratings_total', 'N/A')} reviews)")
        report.append(f"Types: {', '.join(place['types'])}")
        report.append(f"Business Status: {place['business_status']}")
        report.append(f"Currently Open: {'Yes' if place['opening_hours'] else 'No'}")
        report.append("")
    return "\n".join(report)

report = generate_report(places_info)
print(report)

with open('loc_coord.json', 'r') as file:
    location = json.load(file)

# Create map visualization
map_center = location['location'].split(',') # [float(c) for c in location['location'].split(',')]
mymap = folium.Map(location=map_center, zoom_start=15)

# Add markers for each place
marker_cluster = MarkerCluster().add_to(mymap)

for place in places_info:
    folium.Marker(
        location=[place['latitude'], place['longitude']],
        popup=f"{place['name']}<br>Rating: {place.get('rating', 'N/A')}<br>{place['vicinity']}",
        icon=folium.Icon(color='blue' if place['opening_hours'] else 'red')
    ).add_to(marker_cluster)

# Save the map as an HTML file
mymap.save('places_map.html')

# Visualization with Matplotlib
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
