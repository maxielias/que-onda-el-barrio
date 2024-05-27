import json

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

# Display parsed data for verification
for place in places_info:
    print(place)

# Save the extracted information to a new file
with open('places_info.json', 'w') as file:
    json.dump(places_info, file, indent=2)
