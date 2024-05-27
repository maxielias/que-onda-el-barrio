import requests
import os
import json

with open('env/keys.json', 'r') as file:
    data = json.load(file)

API_KEY = data['key'] # os.getenv('GOOGLE_MAPS_API_KEY')
if not API_KEY:
    raise ValueError("API Key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

def get_street_view_image(location, heading, pitch, fov, size, api_key=API_KEY):
    url = f"https://maps.googleapis.com/maps/api/streetview?location={location}&heading={heading}&pitch={pitch}&fov={fov}&size={size}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        with open('street_view.jpg', 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to fetch the image")

with open('loc_coord.json', 'r') as file:
    location = json.load(file)

# Create map visualization
location = location['location']
heading = 0
pitch = 0
fov = 90
size = '640x640'

get_street_view_image(location, heading, pitch, fov, size, api_key=API_KEY)