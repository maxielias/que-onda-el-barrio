import json

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

with open('places_info.json', 'r') as file:
    places_info = json.load(file)
 
report = generate_report(places_info)
print(report)
