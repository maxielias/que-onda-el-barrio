import requests
import json
import os

with open('env/keys.json', 'r') as file:
    data = json.load(file)

API_KEY = data['key'] # os.getenv('GOOGLE_MAPS_API_KEY')
if not API_KEY:
    raise ValueError("API Key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

def get_nearby_places(location, radius=500):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_street_view_image(location, heading=0, pitch=0, fov=90, size='640x640', api_key=API_KEY):
    url = f"https://maps.googleapis.com/maps/api/streetview?location={location}&heading={heading}&pitch={pitch}&fov={fov}&size={size}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        filename = f'street_view_{location.replace(",", "_")}.jpg'
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    return None

location = '-34.57921486683165, -58.4407001669448'
radius = 500  # 500 meters around the location

loc_dict = {
    "location": location,
    "radius": radius
}

print(json.dumps(loc_dict, indent=2))
with open('loc_coord.json', 'w') as file:
    json.dump(loc_dict, file, indent=2) # Save the data to a file

# Get nearby places
places = get_nearby_places(location, radius)
print(json.dumps(places, indent=2))

with open('nearby_places.json', 'w') as file:
    json.dump(places, file, indent=2) # Save the data to a file

# Get street view images
image_file = get_street_view_image(location)
print(f'Street view image saved as {image_file}')