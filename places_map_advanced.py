import os
import json
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import requests

# Get the API key from environment variable
# API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
# if not API_KEY:
#     raise ValueError("API Key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

# def get_nearby_places(location, radius=500):
#     url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={API_KEY}"
#     response = requests.get(url)
#     return response.json()

# def get_street_view_image(location, heading=0, pitch=0, fov=90, size='640x640'):
#     url = f"https://maps.googleapis.com/maps/api/streetview?location={location}&heading={heading}&pitch={pitch}&fov={fov}&size={size}&key={API_KEY}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         filename = f'street_view_{location.replace(",", "_")}.jpg'
#         with open(filename, 'wb') as file:
#             file.write(response.content)
#         return filename
#     return None

with open('loc_coord.json') as file:
    loc_coord = json.load(file)

location = loc_coord['location']
radius = loc_coord['radius']  # 500 meters around the location

# Get nearby places
# places = get_nearby_places(location, radius)
with open('places_info.json') as file:
    places = json.load(file)

# Extract relevant information from the JSON data
places_info = places # []
for place in places['results']:
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

# Create map visualization
map_center = location.split(',')
mymap = folium.Map(location=map_center, zoom_start=15)

# Add markers for each place
marker_cluster = MarkerCluster().add_to(mymap)

for place in places_info:
    folium.Marker(
        location=[place['latitude'], place['longitude']],
        popup=f"{place['name']}<br>Rating: {place.get('rating', 'N/A')}<br>{place['vicinity']}",
        icon=folium.Icon(color='blue' if place['opening_hours'] else 'red')
    ).add_to(marker_cluster)

# Save the map with a right-side container
mymap_html = mymap.get_root().render()

# Create a container for the place information
html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Places Map</title>
    <style>
        #map {{
            width: 75%;
            height: 100vh;
            float: left;
        }}
        #places-container {{
            width: 25%;
            height: 100vh;
            float: right;
            overflow-y: scroll;
            padding: 10px;
            box-sizing: border-box;
            background-color: #f7f7f7;
        }}
        .place {{
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #fff;
        }}
    </style>
</head>
<body>
    <div id="map">{mymap_html}</div>
    <div id="places-container">
    </div>
    <script>
        const places = {json.dumps(places_info)};
        const placesContainer = document.getElementById('places-container');
        places.forEach(place => {{
            const placeDiv = document.createElement('div');
            placeDiv.className = 'place';
            placeDiv.innerHTML = `
                <h3>${{place.name}}</h3>
                <p><strong>Location:</strong> ${{place.latitude}}, ${{place.longitude}}</p>
                <p><strong>Vicinity:</strong> ${{place.vicinity}}</p>
                <p><strong>Rating:</strong> ${{place.rating}} (based on ${{place.user_ratings_total}} reviews)</p>
                <p><strong>Types:</strong> ${{place.types.join(', ')}}</p>
                <p><strong>Business Status:</strong> ${{place.business_status}}</p>
                <p><strong>Currently Open:</strong> ${{place.opening_hours ? 'Yes' : 'No'}}</p>
            `;
            placesContainer.appendChild(placeDiv);
        }});
    </script>
</body>
</html>
'''

# Save the complete HTML file
with open('places_map.html', 'w') as file:
    file.write(html_content)

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
